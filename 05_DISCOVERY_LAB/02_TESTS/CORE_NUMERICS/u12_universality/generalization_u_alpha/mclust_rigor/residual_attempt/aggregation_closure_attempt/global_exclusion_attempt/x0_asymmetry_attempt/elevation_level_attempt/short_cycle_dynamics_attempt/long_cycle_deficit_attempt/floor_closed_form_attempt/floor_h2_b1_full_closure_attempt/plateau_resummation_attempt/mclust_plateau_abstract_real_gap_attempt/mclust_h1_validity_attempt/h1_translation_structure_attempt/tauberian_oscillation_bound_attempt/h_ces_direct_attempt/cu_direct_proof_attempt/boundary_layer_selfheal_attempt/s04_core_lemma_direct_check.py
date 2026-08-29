#!/usr/bin/env python3
"""
s04_core_lemma_direct_check.py -- BOUNDARY-LAYER-SELFHEAL-ATTEMPT

Direct numerical check of the CORE new lemma this front's proof rests on
(ATTEMPT.md Sec 3, Step 4):

  Gamma_u(h) - Gamma(h) := int_0^h e^{-h'/eps}[G'(h'+u)-G'(h')] dh'

  |Gamma_u(h) - Gamma(h)|  <=  3*L1*u     for ALL h,u >= 0

using ONLY (C') (G is L1-Lipschitz) -- via the f-VALUES-ONLY closed form

  Gamma_u(h)-Gamma(h) = e^{-h/eps}[G(h+u)-G(h)] - [G(u)-G(0)]
                         + (1/eps)*int_0^h e^{-h'/eps}[G(h'+u)-G(h')] dh'

(this front's ATTEMPT.md Sec 3 Step 4 derivation) tested against a DIRECT
numerical evaluation of Gamma_u(h) and Gamma(h) themselves (via numerical
differentiation of G to get G', since here -- UNLIKE the main E_full
computation in s03 -- we deliberately want an INDEPENDENT check that goes
through G' explicitly, on a smooth G where G' is unambiguous, as a
cross-check of the closed-form IDENTITY itself, separate from the
Lipschitz-only BOUND it implies).

Two parts:
  Part A: verify the closed-form IDENTITY for Gamma_u(h)-Gamma(h) (via
          G'-based direct computation vs the f-values-only closed form)
          on a smooth test function, where G' is unambiguous.
  Part B: verify the INEQUALITY |Gamma_u(h)-Gamma(h)|<=3*L1*u holds, via
          the f-values-only closed form, across many (h,u,eps) on BOTH a
          smooth Lipschitz G and a kinked (non-C^1) Lipschitz G -- since
          the bound's proof (triangle inequality on 3 Lipschitz-controlled
          pieces) never needed G' to exist anywhere, this must hold on
          kinked G too, and the numerics below (via the values-only
          formula, valid whether or not G' exists) confirm it.
"""
import mpmath as mp

mp.mp.dps = 30


def Gamma_closed_form(G, h, u, eps):
    """Gamma_u(h)-Gamma(h), via the f-VALUES-ONLY closed form (ATTEMPT.md
    Sec 3 Step 4) -- no G' anywhere in this function."""
    h = mp.mpf(h)
    u = mp.mpf(u)
    eps = mp.mpf(eps)
    term1 = mp.e**(-h / eps) * (G(h + u) - G(h))
    term2 = -(G(u) - G(0))
    term3 = (1 / eps) * mp.quad(lambda hp: mp.e**(-hp / eps) * (G(hp + u) - G(hp)), [0, h])
    return term1 + term2 + term3


def Gamma_via_Gprime(Gprime, h, u, eps):
    """Gamma_u(h)-Gamma(h) computed DIRECTLY via G' (only meaningful when
    G is differentiable everywhere on the tested range -- used ONLY in
    Part A, on a smooth G, as an identity cross-check)."""
    h = mp.mpf(h)
    u = mp.mpf(u)
    eps = mp.mpf(eps)
    Gu = mp.quad(lambda hp: mp.e**(-hp / eps) * Gprime(hp + u), [0, h])
    G0 = mp.quad(lambda hp: mp.e**(-hp / eps) * Gprime(hp), [0, h])
    return Gu - G0


print("=" * 78)
print("PART A: closed-form IDENTITY check on a SMOOTH G (G' unambiguous)")
print("        G(a) = sin(2*a) + a/(1+a^2)")
print("=" * 78)


def G_smooth(a):
    a = mp.mpf(a)
    return mp.sin(2 * a) + a / (1 + a**2)


def Gprime_smooth(a):
    a = mp.mpf(a)
    return 2 * mp.cos(2 * a) + (1 - a**2) / (1 + a**2)**2


cases = [
    (mp.mpf('0.3'), mp.mpf('0.05'), mp.mpf('0.2')),
    (mp.mpf('2.0'), mp.mpf('0.5'), mp.mpf('0.5')),
    (mp.mpf('5.0'), mp.mpf('1.5'), mp.mpf('0.1')),
    (mp.mpf('0.1'), mp.mpf('3.0'), mp.mpf('1.0')),
]
for h, u, eps in cases:
    a = Gamma_closed_form(G_smooth, h, u, eps)
    b = Gamma_via_Gprime(Gprime_smooth, h, u, eps)
    reldiff = abs(a - b) / max(abs(b), mp.mpf('1e-30'))
    print(f"  h={float(h):.2f} u={float(u):.2f} eps={float(eps):.2f}  "
          f"closed_form={float(a): .10f}  via_Gprime={float(b): .10f}  "
          f"absdiff={float(abs(a-b)):.3e}")
    assert abs(a - b) < mp.mpf('1e-20'), "Part A FAILED: identity mismatch"
print("PASS: the f-values-only closed form for Gamma_u(h)-Gamma(h) matches")
print("      the direct G'-based computation to > 20 digits at every case.")

print()
print("=" * 78)
print("PART B: the INEQUALITY |Gamma_u(h)-Gamma(h)| <= 3*L1*u, via the")
print("        f-values-only closed form (valid whether or not G' exists")
print("        everywhere), on a SMOOTH G (L1=sup|G'_smooth|) AND on a")
print("        KINKED (non-C^1, still L1-Lipschitz) G")
print("=" * 78)

# smooth G: bound sup|G'| numerically over a generous range to get L1
L1_smooth = mp.mpf(0)
for a in [mp.mpf(v) / 10 for v in range(0, 200)]:
    L1_smooth = max(L1_smooth, abs(Gprime_smooth(a)))
L1_smooth = L1_smooth * mp.mpf('1.01')  # small safety margin over the sampled sup
print(f"  smooth G: using L1 = {float(L1_smooth):.6f} (sampled sup|G'| + 1% margin)")


def G_kinked(a):
    a = mp.mpf(a)
    return mp.mpf('0.4') * abs(a - mp.mpf('0.37')) + mp.mpf('0.6') * abs(a - mp.mpf('1.9')) \
        + a / (2 * (1 + a))


L1_kinked = mp.mpf('0.4') + mp.mpf('0.6') + mp.mpf('0.5')  # two kink slopes + smooth piece's sup|d/da[a/(2(1+a))]|=1/(2(1+a)^2)<=0.5 at a=0
print(f"  kinked G: L1 = {float(L1_kinked):.6f} (exact, by construction)")

test_pts = [
    (mp.mpf('0.5'), mp.mpf('0.001')),
    (mp.mpf('0.5'), mp.mpf('0.01')),
    (mp.mpf('0.5'), mp.mpf('0.1')),
    (mp.mpf('0.5'), mp.mpf('1.0')),
    (mp.mpf('0.5'), mp.mpf('5.0')),
    (mp.mpf('2.0'), mp.mpf('0.05')),
    (mp.mpf('2.0'), mp.mpf('2.0')),
    (mp.mpf('0.05'), mp.mpf('0.3')),
    (mp.mpf('7.0'), mp.mpf('0.5')),
]
eps_test = mp.mpf('0.5')

worst_ratio_smooth = mp.mpf(0)
worst_ratio_kinked = mp.mpf(0)
for h, u in test_pts:
    d_s = abs(Gamma_closed_form(G_smooth, h, u, eps_test))
    bound_s = 3 * L1_smooth * u
    ratio_s = d_s / bound_s if bound_s > 0 else mp.mpf(0)
    worst_ratio_smooth = max(worst_ratio_smooth, ratio_s)

    d_k = abs(Gamma_closed_form(G_kinked, h, u, eps_test))
    bound_k = 3 * L1_kinked * u
    ratio_k = d_k / bound_k if bound_k > 0 else mp.mpf(0)
    worst_ratio_kinked = max(worst_ratio_kinked, ratio_k)

    print(f"  h={float(h):5.2f} u={float(u):6.3f}  "
          f"|diff|_smooth={float(d_s):.4e} bound={float(bound_s):.4e} ratio={float(ratio_s):.4f}  |  "
          f"|diff|_kinked={float(d_k):.4e} bound={float(bound_k):.4e} ratio={float(ratio_k):.4f}")
    assert d_s <= bound_s, f"BOUND VIOLATED (smooth) at h={h},u={u}"
    assert d_k <= bound_k, f"BOUND VIOLATED (kinked) at h={h},u={u}"

print(f"\n  worst-case ratio (smooth G): {float(worst_ratio_smooth):.4f}")
print(f"  worst-case ratio (kinked G): {float(worst_ratio_kinked):.4f}")
print("PASS: |Gamma_u(h)-Gamma(h)| <= 3*L1*u holds at EVERY tested (h,u)")
print("      for both a smooth and a genuinely kinked (non-C^1) Lipschitz")
print("      G -- confirms the core lemma is not an accident of smoothness.")
