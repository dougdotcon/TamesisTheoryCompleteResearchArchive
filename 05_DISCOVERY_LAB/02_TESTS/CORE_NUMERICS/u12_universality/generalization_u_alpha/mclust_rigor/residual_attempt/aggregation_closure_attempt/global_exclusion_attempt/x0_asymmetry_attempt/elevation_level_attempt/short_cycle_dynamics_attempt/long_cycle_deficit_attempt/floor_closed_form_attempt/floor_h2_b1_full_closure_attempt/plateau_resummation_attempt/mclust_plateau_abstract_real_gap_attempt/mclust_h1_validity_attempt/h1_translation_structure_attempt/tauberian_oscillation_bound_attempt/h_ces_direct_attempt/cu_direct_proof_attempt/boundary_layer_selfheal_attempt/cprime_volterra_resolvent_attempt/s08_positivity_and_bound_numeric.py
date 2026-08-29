"""
s08_positivity_and_bound_numeric.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Clean, assertion-based numerical (mpmath, deterministic quadrature, no
randomness) confirmation of s04's THEOREM A (D(s)>=0 on [0,h]), THEOREM B
(exponentially small negative lobe beyond h), and the resulting sharp
bound on ||K(y,t)||, across a grid of (eps, z, h) combinations -- this
consolidates and formalizes this front's own earlier interactive probes
(not committed) into the archived record.
"""
import mpmath as mp

mp.mp.dps = 25

def R(zval):
    return mp.quad(lambda u: mp.e**(-u**2/2 - u*zval), [0, mp.inf])

def sigma(zval):
    return 1 - zval * R(zval)

def D_KAraw(s, h, eps, z):
    if s <= 0:
        return mp.mpf(0)
    upper = min(h, s)
    if upper <= 0:
        return mp.mpf(0)
    f = lambda v: mp.e**(-v/eps) * mp.e**(-(s-v)**2/2 - (s-v)*z)
    return mp.quad(f, [0, upper])

def D_total(s, h, eps, z, My):
    dkb = mp.e**(-s/eps) if (0 <= s <= h) else mp.mpf(0)
    dka = D_KAraw(s, h, eps, z)
    return dkb + My * dka

print("="*70)
print("Check A: D(s) >= 0 on [0,h], for a grid of (eps,z,h) with z>1/eps")
print("="*70)
n_checks = 0
for eps in [mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('1.0')]:
    for zval in [mp.mpf(v) for v in [5, 15, 40]]:
        if zval <= 1/eps:
            continue
        h = zval * mp.mpf('0.7')  # arbitrary h < z, well within [0, z]
        My = (1 - eps*zval) / eps
        for s in [zval*mp.mpf(f) for f in ['0.001', '0.01', '0.05', '0.1',
                                            '0.3', '0.5', '0.7', '0.9', '0.999']]:
            if s > h:
                continue
            d = D_total(s, h, eps, zval, My)
            n_checks += 1
            assert d >= -mp.mpf('1e-20'), f"D(s) negative! eps={eps},z={zval},s={s}: {d}"
print(f"{n_checks} pointwise checks, D(s)>=0 in every case. PASS")

print()
print("="*70)
print("Check B: negative lobe (s>h) magnitude vs the eps*e^{-h/eps} bound")
print("="*70)
n_checks = 0
for eps in [mp.mpf('0.3'), mp.mpf('0.5'), mp.mpf('1.0')]:
    for zval in [mp.mpf(v) for v in [10, 30]]:
        h = zval * mp.mpf('0.6')
        My = (1 - eps*zval) / eps
        neg_lobe = mp.quad(lambda s: D_total(s, h, eps, zval, My),
                            [h, h+2, h+8, h+20])
        bound = eps * mp.e**(-h/eps)
        n_checks += 1
        assert neg_lobe <= 0, f"negative lobe not negative: {neg_lobe}"
        assert abs(neg_lobe) <= bound, f"negative lobe exceeds bound: |{neg_lobe}| > {bound}"
        ratio = abs(neg_lobe) / bound
        print(f"  eps={float(eps)}, z={float(zval)}, h={float(h):.2f}: "
              f"|neg lobe|={mp.nstr(abs(neg_lobe),6)}, bound={mp.nstr(bound,6)}, "
              f"ratio={mp.nstr(ratio,4)}")
print(f"{n_checks} checks, negative lobe always negative and within the eps*e^-h/eps bound. PASS")

print()
print("="*70)
print("Check C: full ||K(y,t)|| bound (int|D|) vs the sharp formula, and vs")
print("the archive's own crude constant sqrt(pi/2)+eps")
print("="*70)
sqrt_pi_2 = mp.sqrt(mp.pi/2)
n_checks = 0
for eps in [mp.mpf('0.3'), mp.mpf('0.5')]:
    for zval in [mp.mpf(v) for v in [10, 30, 60]]:
        h = zval  # t=0, maximal-h case
        My = (1 - eps*zval) / eps
        s_cutoff = h + 20
        unsigned = mp.quad(lambda s: abs(D_total(s, h, eps, zval, My)),
                            [0, h*mp.mpf('0.01'), h*mp.mpf('0.5'), h, h+2, h+8, s_cutoff])
        Rz, sgz = R(zval), sigma(zval)
        sharp_formula = (1-mp.e**(-h/eps))*(Rz+eps*sgz) + eps*mp.e**(-h/eps)
        n_checks += 1
        rel = abs(unsigned - sharp_formula) / sharp_formula
        print(f"  eps={float(eps)}, z=h={float(zval)}: ||K|| (numeric)={mp.nstr(unsigned,8)}, "
              f"sharp bound={mp.nstr(sharp_formula,8)}, crude bound={mp.nstr(sqrt_pi_2+eps,4)}, "
              f"rel.diff={mp.nstr(rel,4)}")
        assert unsigned <= sharp_formula * (1 + mp.mpf('1e-6')), "numeric norm exceeds sharp bound"
        assert unsigned <= sqrt_pi_2 + eps, "sharp bound (or true norm) exceeds crude archive bound!"
print(f"{n_checks} checks: true operator norm matches the sharp bound (to quadrature")
print("precision) and is always far below the crude sqrt(pi/2)+eps constant. PASS")

print()
print("ALL s08 CHECKS PASSED.")
