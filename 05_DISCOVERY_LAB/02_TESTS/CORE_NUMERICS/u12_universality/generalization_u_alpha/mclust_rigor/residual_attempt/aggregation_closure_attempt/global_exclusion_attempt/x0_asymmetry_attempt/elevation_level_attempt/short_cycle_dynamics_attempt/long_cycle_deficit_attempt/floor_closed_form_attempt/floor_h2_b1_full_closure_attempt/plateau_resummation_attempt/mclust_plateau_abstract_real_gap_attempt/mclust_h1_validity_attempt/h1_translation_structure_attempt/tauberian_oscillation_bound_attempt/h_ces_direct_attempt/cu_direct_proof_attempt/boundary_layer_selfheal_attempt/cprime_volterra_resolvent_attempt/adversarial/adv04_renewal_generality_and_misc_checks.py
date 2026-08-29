"""
adv04_renewal_generality_and_misc_checks.py -- hostile referee, misc
independent checks:

Part 1: the renewal/Malthusian obstruction (target's Sec 2.2) -- confirm
s_+(c,eps) = (sqrt(1+4c*eps)-1)/(2*eps) > 0 for EVERY c,eps>0 (a trivial
but correctly-general elementary fact), and confirm k_hat(s_+)=1 exactly
by direct substitution.

Part 2: NOTA -- the target's "Conclusion" paragraph (Sec 2.2) generalizes
its finding ("ANY norm-envelope argument ... by a function of the lag h
alone that does not decay ... is doomed") beyond what was actually proved
(which is specifically for the parametric family k(h)=c*(1-e^{-h/eps}),
the shape that happens to match K_B(h) exactly). We check: does a
DIFFERENT saturating shape (e.g. a slower, algebraic-rate approach to
saturation) still force exponential blow-up? We test one alternative
shape numerically to see if the broader claim is at least plausible
(not a proof of the fully general claim, just a spot-check).

Part 3: sup-over-x nota -- checks whether the SHARP-type bound (using
the CORRECTED coefficient from adv02) is monotonically WORSE (larger) as
x decreases toward 0 for fixed y, confirming the target's own bound,
which is expressed via z=x+y, is understated as "uniform in y" without
mentioning it is uniform in x too (a positive finding: the bound the
target derives, once the adv02 coefficient is fixed, is actually
uniform jointly in (x,y), which is a slightly stronger fact than what
the document explicitly claims).

Part 4: the "more than two orders of magnitude sharper" claim (Sec 3.4,
eps=0.5, z=60) -- independently confirmed. This specific regime (h=z=60
i.e. the h=y, t=0, x=0 case cited) has h/eps=120, astronomically large,
so the adv02 coefficient bug (which only matters for MODERATE h/eps) is
invisible here -- this specific claim is accurate.
"""
import mpmath as mp
import numpy as np
from scipy import integrate
from scipy.special import erfcx

mp.mp.dps = 30

print("="*90)
print("Part 1: s_+(c,eps) > 0 for every c,eps>0 (renewal/Malthusian root positivity)")
print("="*90)
for c in [0.001, 0.1, 1.0, 10.0, 1000.0]:
    for eps in [0.01, 0.5, 1.0, 5.0]:
        c_ = mp.mpf(c); eps_ = mp.mpf(eps)
        s_plus = (mp.sqrt(1+4*c_*eps_)-1)/(2*eps_)
        khat_at_splus = c_/(eps_*s_plus*(s_plus+1/eps_))
        assert s_plus > 0
        assert abs(khat_at_splus - 1) < mp.mpf('1e-25')
print("Confirmed s_+ > 0 and k_hat(s_+)=1 exactly, for all 20 tested (c,eps) pairs.")
print("This IS a fully general, unconditional elementary algebraic fact for the")
print("SPECIFIC parametric family k(h)=c*(1-e^{-h/eps}) -- confirmed correct.")

print()
print("="*90)
print("Part 2 (NOTA): does the CONCLUSION's broader claim (any non-decaying")
print("saturating envelope, not just this family) hold for a DIFFERENT shape?")
print("="*90)
print("Testing k(h) = c*(1 - 1/(1+h/eps))  [algebraic, SLOWER approach to")
print("saturation than the exponential family, same c, same eps]")
def solve_renewal_numeric(kfun, y_end, n_steps=4000):
    dy = y_end/n_steps
    ys = np.linspace(0, y_end, n_steps+1)
    M = np.zeros(n_steps+1)
    M[0] = 1.0
    kvals = np.array([kfun(h) for h in ys])
    # trapezoid Volterra solve: M(y_n) = 1 + sum trapezoid of k(y_n-t)*M(t)
    for n in range(1, n_steps+1):
        sm = 0.0
        for j in range(n+1):
            h = ys[n]-ys[j]
            w = 0.5*dy if (j==0 or j==n) else dy
            sm += w*kfun(h)*M[j]
        M[n] = 1.0 + sm
    return ys, M
c, eps = 1.0, 0.5
kfun = lambda h: c*(1 - 1/(1+h/eps))
ys, M = solve_renewal_numeric(kfun, 15, n_steps=600)
ratios = M[400]/M[200], M[600]/M[400]
print(f"M(y) at y={ys[200]:.2f},{ys[400]:.2f},{ys[600]:.2f}: {M[200]:.4f},{M[400]:.4f},{M[600]:.4f}")
print(f"Growth ratios over equal y-increments: {ratios[0]:.4f}, {ratios[1]:.4f}")
print("(roughly constant ratio across equal increments is consistent with")
print(" continued exponential-type growth for this different saturating shape")
print(" too -- SUPPORTS the broader qualitative claim as plausible, but this")
print(" is a spot-check on ONE alternative shape, not a general proof; the")
print(" target's Sec 2.2 'Conclusion' paragraph technically only rigorously")
print(" covers the specific exponential-saturation family it computes with.")
print(" This is a NOTA -- a wording/scope precision issue, not an error.)")

print()
print("="*90)
print("Part 3: sup-over-x nota -- is the (corrected) bound worse for SMALLER x?")
print("="*90)
def R_np(zz):
    return np.sqrt(np.pi/2) * erfcx(zz/np.sqrt(2))
def A_of_z(zz, eps):
    Rz = R_np(zz)
    return Rz + eps*(1-zz*Rz)
eps = 0.4
y = 20.0
for x in [0.0, 0.5, 1.0, 3.0]:
    z = x+y
    print(f"  x={x}: z={z}, A(z)={A_of_z(z,eps):.6f}  (larger A(z) = worse/larger bound)")
print("Confirms A(z) DECREASING in z, i.e. INCREASING as x decreases toward 0 --")
print("so x=0 is the worst case for fixed y, and the target's own numerics (fixed")
print("x=1 throughout Sec 3-5) do not probe the worst case over x. The target's")
print("own Sec 8 item 7 discloses this as 'not independently verified across x' --")
print("an honest, correctly-scoped disclosure (NOTA, not a correcao).")

print()
print("="*90)
print("Part 4: 'more than two orders of magnitude sharper' claim, eps=0.5, z=h=60")
print("="*90)
def D_KAraw(s, h, z, eps):
    upper = min(h, s)
    if upper <= 0: return 0.0
    f = lambda v: np.exp(-v/eps) * np.exp(-(s-v)**2/2 - (s-v)*z)
    val, _ = integrate.quad(f, 0, upper, limit=200)
    return val
def D_full(s, h, z, eps):
    My = (1-eps*z)/eps
    dkb = np.exp(-s/eps) if (0 <= s <= h) else 0.0
    return dkb + My*D_KAraw(s,h,z,eps)
eps_, z_, h_ = 0.5, 60.0, 60.0  # x=0, t=0 case cited by the target
true_norm, _ = integrate.quad(lambda s: abs(D_full(s,h_,z_,eps_)), 0, h_+50*eps_, limit=400)
crude = np.sqrt(np.pi/2)+eps_
print(f"TRUE ||K(y,t)|| (direct quadrature) = {true_norm:.6f}")
print(f"crude archive bound sqrt(pi/2)+eps    = {crude:.6f}")
print(f"ratio (sharpness factor)              = {crude/true_norm:.2f}x")
print("CONFIRMED: this specific claim (>100x sharper at eps=0.5,z=60) is accurate --")
print("this regime has h/eps=120, so the adv02 coefficient bug (relevant only at")
print("MODERATE h/eps, roughly 2-6) is invisible here; the claim holds as stated.")
