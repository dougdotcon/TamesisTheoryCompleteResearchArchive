# Hostile-referee check 3 (extension front): OWN independent end-to-end assembly of
#   D*(p)_r(b) = (1/2)[Phi_b(r) M_p(N) - Strip_p(r,b)] - sum_{k=1}^p o_k H_{2k-1}(r,b)/2^{2k-1}
# (the accepted, wave-15-refereed formula), built from THIS REFEREE'S OWN ingredient
# routes -- all different from the front's:
#   * Q_p(u): DP values of e_p(1..u) + exact Newton-divided-difference interpolation
#             (NOT Newton's identities -- the wave-15 referee's methodology, rebuilt fresh);
#   * mu_{2l}(N): this referee's own power-series-exponentiation implementation
#             (ref_moments.py), itself validated against direct binomial summation l=1..20;
#   * H_{2k-1}(r,b) = A_k(N,r)/(r+1): this referee's own polynomial factorization route
#             (ref_hk.py), itself validated against brute-force P_b*S summation;
#   * Phi_b, Strip weights w_i: direct factorial arithmetic;
# checked against this referee's OWN Corollary A3 ground truth (ref_ground_truth.py).
# The front's production code was never read, let alone executed. sp.nsimplify is
# nowhere in this referee's call graph (trivially: sympy is not even imported here).
# Exact arithmetic only (fractions.Fraction + Python ints). No randomness.

from fractions import Fraction
from math import comb, factorial
import pickle
import os
import sys
import time

sys.setrecursionlimit(10000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ref_moments
import ref_ground_truth as gt

KMAX = 20
ACACHE = os.path.join(HERE, "ref_A_cache.pkl")


# ---------- ingredient 1: Q_p(u) by DP + exact interpolation ----------

def ep_values(p, umax):
    """e_p(1,...,u) for u=0..umax via the DP e_j(1..u) = e_j(1..u-1) + u*e_{j-1}(1..u-1)."""
    e = [0] * (p + 1)
    e[0] = 1
    vals = [e[p]]
    for u in range(1, umax + 1):
        for j in range(min(p, u), 0, -1):
            e[j] = e[j] + u * e[j - 1]
        vals.append(e[p])
    return vals


def newton_interp_coeffs(xs, ys):
    """Exact interpolation -> standard-basis coefficient list (Fractions)."""
    n = len(xs)
    dd = [Fraction(y) for y in ys]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            dd[i] = (dd[i] - dd[i - 1]) / (xs[i] - xs[i - j])
    # expand Newton form to standard basis
    coeffs = [Fraction(0)] * n
    coeffs[0] = dd[n - 1]
    deg = 0
    for i in range(n - 2, -1, -1):
        # multiply current poly by (x - xs[i]) and add dd[i]
        new = [Fraction(0)] * (deg + 2)
        for t in range(deg + 1):
            new[t + 1] += coeffs[t]
            new[t] -= coeffs[t] * xs[i]
        new[0] += dd[i]
        deg += 1
        coeffs = new + [Fraction(0)] * (n - len(new))
    return coeffs[:2 * 1000]


def Q_poly(p):
    """Coefficient list (len 2p+1) of Q_p(u), by interpolation through u=0..2p."""
    if p == 0:
        return [Fraction(1)]
    xs = list(range(0, 2 * p + 1))
    ys = ep_values(p, 2 * p)
    coeffs = newton_interp_coeffs(xs, ys)[:2 * p + 1]
    # sanity: reproduces DP values BEYOND the interpolation nodes (u = 2p+1 .. 2p+6)
    ys_ext = ep_values(p, 2 * p + 6)
    for u in range(0, 2 * p + 7):
        acc = Fraction(0)
        for c in reversed(coeffs):
            acc = acc * u + c
        assert acc == ys_ext[u], ("Q interp failed", p, u)
    assert coeffs[-1] != 0
    return coeffs


def shifted_coeffs(qcoeffs, c):
    """Coefficients in v of Q(-(v+c)):  coeff_t = sum_n q_n (-1)^n C(n,t) c^{n-t}."""
    n = len(qcoeffs)
    out = [Fraction(0)] * n
    for ni, q in enumerate(qcoeffs):
        if q == 0:
            continue
        sgn = -1 if ni % 2 else 1
        for t in range(0, ni + 1):
            out[t] += q * sgn * comb(ni, t) * c ** (ni - t)
    return out


# ---------- ingredient 2: mu polynomials (referee's own, validated) ----------

MUS = ref_moments.mu_polys(KMAX)   # {l: coeff list in N}


def M_p_at(e_even, N):
    """M_p(N) = sum_l e_{2l} mu_{2l}(N), mu_0 = 1."""
    acc = e_even[0]
    for l in range(1, len(e_even)):
        if e_even[l] != 0:
            acc += e_even[l] * ref_moments.poly_eval(MUS[l], N)
    return acc


# ---------- ingredient 3: H_{2k-1}(r,b) via referee's A_k factorization ----------

def load_A_dicts():
    if os.path.exists(ACACHE):
        with open(ACACHE, "rb") as fh:
            return pickle.load(fh)
    import ref_hk
    A = ref_hk.build_A_polys(KMAX)
    out = {}
    for k, poly in A.items():
        d = {}
        for (iN, im), coef in zip(poly.monoms(), poly.coeffs()):
            d[(iN, im)] = int(coef)
        out[k] = d
    with open(ACACHE, "wb") as fh:
        pickle.dump(out, fh)
    return out


ADICTS = load_A_dicts()
MAXDEGN = max(iN for d in ADICTS.values() for (iN, im) in d)
MAXDEGM = max(im for d in ADICTS.values() for (iN, im) in d)


def H_val(k, r, b):
    N = 2 * r + b + 1
    pN = [1] * (MAXDEGN + 1)
    for i in range(1, MAXDEGN + 1):
        pN[i] = pN[i - 1] * N
    pM = [1] * (MAXDEGM + 1)
    for i in range(1, MAXDEGM + 1):
        pM[i] = pM[i - 1] * r
    acc = 0
    for (iN, im), coef in ADICTS[k].items():
        acc += coef * pN[iN] * pM[im]
    return Fraction(acc, r + 1)


# ---------- the assembly ----------

FACT = {}


def fact(n):
    if n not in FACT:
        FACT[n] = factorial(n)
    return FACT[n]


class Assembly:
    def __init__(self, p, b):
        self.p, self.b = p, b
        beta = b + 1
        c = Fraction(beta, 2)
        q = Q_poly(p)
        d = shifted_coeffs(q, c)            # Q_p(-(v+beta/2)) coefficients in v
        self.e_even = [d[2 * l] for l in range(0, p + 1)]
        self.o_odd = [d[2 * k - 1] for k in range(1, p + 1)]  # o_1..o_p
        # E_p as full even polynomial for Strip evaluation
        self.E_coeffs = [d[t] if t % 2 == 0 else Fraction(0) for t in range(len(d))]
        # per-k H powers cache built on the fly
        # precompute powers of N needed for A evaluation once per (r) in D()
        self.maxdegN = max((iN for k in range(1, p + 1)
                            for (iN, im) in ADICTS[k]), default=0)
        self.maxdegM = max((im for k in range(1, p + 1)
                            for (iN, im) in ADICTS[k]), default=0)

    def E_at(self, x):
        acc = Fraction(0)
        for cf in reversed(self.E_coeffs):
            acc = acc * x + cf
        return acc

    def D(self, r):
        p, b = self.p, self.b
        N = 2 * r + b + 1
        beta = b + 1
        # M_p(N)
        M = M_p_at(self.e_even, N)
        # Phi_b(r) = P_b 2^N
        Phi = Fraction(fact(r) * fact(r + b) * 2 ** N, fact(N))
        # Strip
        strip = Fraction(0)
        for i in range(1, b + 1):
            w = Fraction(fact(r) * fact(r + b), fact(r + i) * fact(r + b + 1 - i))
            strip += self.E_at(i - Fraction(beta, 2)) * w
        # odd part
        pN = [1] * (self.maxdegN + 1)
        for t in range(1, self.maxdegN + 1):
            pN[t] = pN[t - 1] * N
        pM = [1] * (self.maxdegM + 1)
        for t in range(1, self.maxdegM + 1):
            pM[t] = pM[t - 1] * r
        odd = Fraction(0)
        for k in range(1, p + 1):
            acc = 0
            for (iN, im), coef in ADICTS[k].items():
                acc += coef * pN[iN] * pM[im]
            Hk = Fraction(acc, r + 1)
            odd += self.o_odd[k - 1] * Hk / 2 ** (2 * k - 1)
        return (Phi * M - strip) / 2 - odd


def sweep(p, r_range, b_range, label=""):
    t0 = time.time()
    checks = fails = 0
    for b in b_range:
        asm = Assembly(p, b)
        for r in r_range:
            got = asm.D(r)
            want = gt.D_star(p, r, b)
            checks += 1
            if got != want:
                fails += 1
                print(f"  MISMATCH p={p} r={r} b={b}: assembly={got} A3={want}")
    dt = time.time() - t0
    print(f"p={p} {label}: {checks} checks, fails={fails}, time={dt:.1f}s")
    return checks, fails


def main():
    total_checks = total_fails = 0

    # ---- gate 0: calibration p=1..4 (must reproduce PROVED territory exactly) ----
    print("--- calibration gate: p=1..4 vs referee ground truth ---")
    for p in (1, 2, 3, 4):
        c, f = sweep(p, [0, 1, 2, 3, 7, 15, 40], range(0, 11), label="calibration")
        total_checks += c
        total_fails += f
    assert total_fails == 0

    # ---- gate 0b: the section-2.4 disclosed bug's stated TRUE value ----
    v = gt.D_star(3, 15, 0)
    print(f"D*(3)_15(0) via referee A3 = {v} "
          f"(front's section 2.4 claims 1143904849/80144052: "
          f"{'MATCH' if v == Fraction(1143904849, 80144052) else 'MISMATCH'})")
    assert v == Fraction(1143904849, 80144052)

    # ---- main sweeps: p=11..20 ----
    # Referee's coverage choice: FULL r=0..200 x b=0..30 for every p (matching the
    # front's claimed scale exactly), entirely with referee-built machinery.
    print("--- main sweeps: p=11..20, r=0..200, b=0..30 (full) ---")
    for p in range(11, 21):
        c, f = sweep(p, range(0, 201), range(0, 31), label="r=0..200,b=0..30")
        total_checks += c
        total_fails += f

    # ---- scale push beyond the front's own ceiling: r up to 300 ----
    # (the front's section 6 suggested exactly this, mirroring the wave-15 referee's
    # own scale-push methodology; done here for the two largest p values printed
    # in the log's b>=2 blocks, p=15 and p=20, and at every b=0..30)
    print("--- scale push: r=201..300, b=0..30, p=15 and p=20 ---")
    for p in (15, 20):
        c, f = sweep(p, range(201, 301), range(0, 31), label="r=201..300,b=0..30 SCALE PUSH")
        total_checks += c
        total_fails += f

    print(f"TOTAL: {total_checks} checks, fails={total_fails}")
    assert total_fails == 0
    print("ALL REFEREE ASSEMBLY SWEEPS PASSED (p=11..20 full r<=200/b<=30; "
          "p=15,20 pushed to r=300)")


if __name__ == "__main__":
    main()
