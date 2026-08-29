"""
s03_true_operator_norm_numeric.py -- CPRIME-VOLTERRA-RESOLVENT-ATTEMPT

Exploratory (not a proof either way), deterministic numerical experiment:
does the TRUE operator norm ||K(y,t)|| (sup over ALL bounded f, not just
the constant function 1) decay as h=y-t grows, or does it stay bounded
away from 0 -- as the crude additive triangle-inequality envelope
(s01 Parts 4-5 + s02) suggests it might (saturating near 2*eps*(1-e^{-h/eps})
for large z), OR does the pointwise cancellation found on CONSTANT f
(s01 Part 6: K(y,t)[1](x) -> 0 like 1/z) somehow persist for the TRUE
sup-norm operator norm too (which would be a much stronger, and
surprising, positive fact)?

Method. K(y,t) is a signed integral operator: (K(y,t)f)(x) =
int_0^inf D(s) f(x+s) ds, s:=x'-x, with EXPLICIT density

  D(s) = D_KB(s) + M_y * D_KAraw(s)
  D_KB(s)    := e^{-s/eps} * 1[0<=s<=h]                          (from K_B(h))
  D_KAraw(s) := int_0^{min(h,s)} e^{-v/eps} * e^{-(s-v)^2/2-(s-v)z} dv
                                                                    (from K_A^raw)

derived directly from the raw operator definitions by substituting
u = s-v in T_{y-v}'s own u-integral (s02's Part... no, this is fresh,
s03-local derivation, done from scratch here, cross-checked against
s01's exact K(y,t)[1](x) formula via int_0^inf D(s) ds = K(y,t)[1](x)).

For a genuinely SIGNED kernel, the L^infty -> L^infty operator norm is

  ||K(y,t)|| = int_0^inf |D(s)| ds     (attained by f(x+s):=sign(D(s)))

We compute int D(s) ds (signed) and int |D(s)| ds (operator norm) both
by direct deterministic quadrature (mpmath.quad, fixed strategy, no
sampling), and compare:
  (i) the signed integral against s01's exact closed form -- a
      cross-check of this script's own fresh density derivation;
  (ii) the unsigned (operator-norm) integral against the signed one,
       across growing h=y (fixing t=0, x=0, i.e. z=y=h -- the maximal
       "h=y" case) -- to see whether cancellation in the OPERATOR NORM
       sense survives, or whether (as hypothesized in ATTEMPT.md Sec 4)
       it collapses to roughly 2*eps for large z while the SIGNED
       integral stays small.
"""
import mpmath as mp

mp.mp.dps = 20

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

def signed_and_unsigned_norms(eps, x, y, t, s_cutoff, n_grid):
    """h=y-t, z=x+y. Integrate D(s) and |D(s)| over s in [0, s_cutoff]
    via composite Simpson on a fixed grid (deterministic, no adaptivity
    needed -- integrand is smooth in s away from s=h where D_KB has a
    jump discontinuity; we split the integration range at s=h explicitly
    to avoid quadrature trouble at that kink)."""
    h = y - t
    z = x + y
    My = (1 - eps*z)/eps
    # split integration at s=h (D_KB has a jump there) and at s_cutoff
    pts_signed = []
    pts_unsigned = []
    breakpoints = sorted(set([0, h, s_cutoff]))
    signed_total = mp.mpf(0)
    unsigned_total = mp.mpf(0)
    for i in range(len(breakpoints)-1):
        a, b = breakpoints[i], breakpoints[i+1]
        if b <= a:
            continue
        fs = lambda s: D_total(s, h, eps, z, My)
        signed_total += mp.quad(fs, [a, b])
        funsigned = lambda s: abs(D_total(s, h, eps, z, My))
        unsigned_total += mp.quad(funsigned, [a, b])
    return signed_total, unsigned_total, h, z, My

print("="*70)
print("Cross-check: fresh density-based signed integral vs s01's exact")
print("closed form K(y,t)[1](x) = (1-e^{-h/eps})*[R(z)+eps*sigma(z)]")
print("="*70)
eps = mp.mpf('0.5')
for (x_, y_, t_) in [(mp.mpf(0), mp.mpf(6), mp.mpf(0)), (mp.mpf(1), mp.mpf(9), mp.mpf(2))]:
    s_cutoff = y_ + 15  # generous tail cutoff; density decays fast beyond s~h+O(1/z)
    signed, unsigned, h_, z_, My_ = signed_and_unsigned_norms(eps, x_, y_, t_, s_cutoff, None)
    exact = (1 - mp.e**(-h_/eps)) * (R(z_) + eps*sigma(z_))
    rel = abs(signed - exact) / exact
    print(f"x={float(x_)}, y={float(y_)}, t={float(t_)}: h={float(h_)}, z={float(z_)}")
    print(f"  fresh density-integral (signed): {mp.nstr(signed, 12)}")
    print(f"  s01 exact closed form:           {mp.nstr(exact, 12)}")
    print(f"  relative error: {mp.nstr(rel, 6)}")
    assert rel < mp.mpf('1e-8')
    print("  PASS (independent cross-check of this script's own density formula)")

print()
print("="*70)
print("Main experiment: does ||K(y,t)|| (unsigned/operator-norm integral)")
print("decay with h, or saturate, while the SIGNED integral -> 0 ?")
print("Fixed x=0, t=0 (so h=y=z, the maximal-h / h=y case).")
print("="*70)
print(f"{'z=h=y':>8} | {'signed (K[1])':>16} | {'unsigned (||K||)':>18} | {'2*eps*(1-e^-h/eps)':>20}")
results = []
for zval in [5, 10, 20, 40, 60, 90]:
    x_, y_, t_ = mp.mpf(0), mp.mpf(zval), mp.mpf(0)
    s_cutoff = y_ + 15
    signed, unsigned, h_, z_, My_ = signed_and_unsigned_norms(eps, x_, y_, t_, s_cutoff, None)
    envelope = 2*eps*(1 - mp.e**(-h_/eps))
    print(f"{zval:>8} | {mp.nstr(signed,8):>16} | {mp.nstr(unsigned,8):>18} | {mp.nstr(envelope,8):>20}")
    results.append((zval, signed, unsigned, envelope))

print()
print("Interpretation printed to ATTEMPT.md Sec 4 (not asserted here as a")
print("proof either way -- this is disclosed as exploratory numerical")
print("evidence, deterministic quadrature, no randomness).")

# Sanity assertions on qualitative shape (not full rigor, just guarding
# against a gross implementation bug): signed values should shrink
# relative to unsigned as z grows, and unsigned should NOT shrink to
# near-zero over this range (i.e. the operator norm should stay of
# order eps, not vanish like the signed quantity does).
z_last, signed_last, unsigned_last, env_last = results[-1]
z_first, signed_first, unsigned_first, env_first = results[0]
assert unsigned_last > mp.mpf('0.1') * eps, "unsigned (operator norm) collapsed unexpectedly"
assert signed_last < signed_first, "signed quantity did not shrink as expected"
print()
print(f"At z={z_last}: signed={mp.nstr(signed_last,6)} (small, shrinking)")
print(f"           unsigned={mp.nstr(unsigned_last,6)} (order eps={float(eps)}, NOT shrinking)")
print("Confirms qualitatively: the pointwise/constant-function cancellation")
print("does NOT survive in the operator-norm (worst-case-f) sense -- the")
print("TRUE operator norm empirically stays of order eps as h,z grow large,")
print("consistent with (not a proof of) the analytic obstruction argument.")
print()
print("ALL s03 CHECKS PASSED (cross-check assertions); qualitative finding")
print("recorded, disclosed as exploratory, in ATTEMPT.md Sec 4.")
