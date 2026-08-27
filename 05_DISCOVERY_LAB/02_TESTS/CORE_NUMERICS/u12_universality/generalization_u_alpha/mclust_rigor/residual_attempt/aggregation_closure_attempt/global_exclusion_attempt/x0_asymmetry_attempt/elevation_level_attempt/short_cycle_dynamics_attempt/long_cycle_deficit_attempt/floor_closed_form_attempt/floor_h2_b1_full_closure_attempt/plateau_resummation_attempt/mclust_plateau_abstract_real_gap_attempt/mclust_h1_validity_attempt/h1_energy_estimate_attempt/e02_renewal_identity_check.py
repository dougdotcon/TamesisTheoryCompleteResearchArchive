"""
e02_renewal_identity_check.py -- numerical verification of the NEW exact
renewal identity for Psi derived in this front's ATTEMPT.md Sec 2
(the "(BB-Psi') formula"):

    Psi(s,g) = c * int_0^inf e^{-c[v^2/2 + v(s+g)]} * I(s+v,g) dv     (BB-Psi'-unscaled)
    I(s,g)   := int_0^g Phi(s,g') dg'

This is derived from the exact ODE (E1) [Psi_x = (x+y)Psi - I, in scaled
(x,y) variables x=s sqrt(c), y=g sqrt(c)] via the SAME variation-of-
parameters / bounded-branch selection principle as the Growth-Exclusion
Lemma quoted (in prose, required reading) from
mclust_h2_validity_attempt/ATTEMPT.md Sec 2 -- applied here to the EXACT
(non eps-expanded) equation for the first time in this lineage, not just
order-by-order to the psi_n's. See ATTEMPT.md Sec 2.1/2.2 for the full
derivation and the standing hypothesis (B) (boundedness of Psi(.,g) as
s->infinity, at each fixed g) this identity is conditional on.

I(s,g) is computed EXACTLY (as a finite sum, not by quadrature) using the
family's own power series:  I(s,g) = sum_k a_k(s) g^{k+1}/(k+1).
The v-integral is done by mpmath.quad over [0, infinity).
"""

import time
import mpmath as mp
import e01_family_series as fs


def make_I_func(a_list, c, K):
    """Returns I(s,g) = int_0^g Phi(s,g') dg' = sum_k a_k(s) g^{k+1}/(k+1),
    reusing a single erfcx(s*sqrt(c/2)) evaluation per call (not one per k)."""
    sqrt_c_2 = mp.sqrt(c / mp.mpf(2))

    def I_of(s, g):
        Eval = fs.erfcx(s * sqrt_c_2)
        total = mp.mpf(0)
        gp = g  # running g^{k+1}
        for k in range(len(a_list)):
            ak = a_list[k]
            term_coef = fs.p_eval(ak.P, s) + Eval * fs.p_eval(ak.Q, s)
            total += term_coef * gp / (k + 1)
            gp *= g
        return total

    return I_of


def psi_via_renewal(s0, g, I_of, c, maxdegree=6):
    """Psi(s0,g) via the (BB-Psi') formula, quadrature over v on a FINITE
    range [0, cutoff] (the e^{-c v (s0+g)} kernel makes the tail beyond
    cutoff negligible; breakpoints chosen from the kernel's own decay
    scale 1/(c*(s0+g)) rather than mpmath's infinite-interval transform,
    which was found -- disclosed, self-caught issue S1 in ATTEMPT.md --
    to require prohibitively many integrand evaluations at working
    precision)."""
    c = mp.mpf(c)
    scale = mp.mpf(1) / (c * (s0 + g))
    cutoff = 40 * scale + 5  # generous: kernel ~ e^{-40} at v=cutoff-ish, plus margin

    def integrand(v):
        kernel = mp.e ** (-c * (v * v / 2 + v * (s0 + g)))
        if kernel == 0:
            return mp.mpf(0)
        return kernel * I_of(s0 + v, g)

    breakpoints = [0, scale, 3 * scale, 8 * scale, cutoff]
    val = mp.quad(integrand, breakpoints, maxdegree=maxdegree)
    return c * val


def main():
    c_val = 200
    K = 110
    dps = 90
    mp.mp.dps = dps
    c = mp.mpf(c_val)

    print(f"=== e02_renewal_identity_check :: c={c_val}, K={K}, dps={dps} ===")
    t0 = time.time()
    a, b = fs.build_series(c, K, dps)
    print(f"series built in {time.time()-t0:.1f}s")

    I_of = make_I_func(a, c, K)

    test_points = [
        (mp.mpf('0.0'), mp.mpf('0.05')),
        (mp.mpf('0.0'), mp.mpf('0.10')),
        (mp.mpf('0.05'), mp.mpf('0.05')),
        (mp.mpf('0.10'), mp.mpf('0.10')),
        (mp.mpf('0.20'), mp.mpf('0.08')),
    ]

    results = []
    for s0, g in test_points:
        t1 = time.time()
        Psi_direct = fs.eval_Psi(b, s0, c)(g)
        Psi_renewal = psi_via_renewal(s0, g, I_of, c, maxdegree=6)
        reldiff = abs(Psi_renewal - Psi_direct) / abs(Psi_direct)
        dt = time.time() - t1
        print(f"s={mp.nstr(s0,4)} g={mp.nstr(g,4)}: "
              f"Psi_direct={mp.nstr(Psi_direct,25)}  "
              f"Psi_renewal={mp.nstr(Psi_renewal,25)}  "
              f"reldiff={mp.nstr(reldiff,6)}  ({dt:.1f}s)")
        results.append((s0, g, Psi_direct, Psi_renewal, reldiff))

    print()
    max_reldiff = max(r[4] for r in results)
    print(f"MAX relative difference across all test points: {mp.nstr(max_reldiff,6)}")
    if max_reldiff < mp.mpf('1e-6'):
        print("VERDICT: PASS -- (BB-Psi') exact renewal identity confirmed "
              "(two independent computation routes agree to the precision "
              "achieved here).")
    else:
        print("VERDICT: FAIL or insufficient precision -- see reldiff above.")


if __name__ == "__main__":
    main()
