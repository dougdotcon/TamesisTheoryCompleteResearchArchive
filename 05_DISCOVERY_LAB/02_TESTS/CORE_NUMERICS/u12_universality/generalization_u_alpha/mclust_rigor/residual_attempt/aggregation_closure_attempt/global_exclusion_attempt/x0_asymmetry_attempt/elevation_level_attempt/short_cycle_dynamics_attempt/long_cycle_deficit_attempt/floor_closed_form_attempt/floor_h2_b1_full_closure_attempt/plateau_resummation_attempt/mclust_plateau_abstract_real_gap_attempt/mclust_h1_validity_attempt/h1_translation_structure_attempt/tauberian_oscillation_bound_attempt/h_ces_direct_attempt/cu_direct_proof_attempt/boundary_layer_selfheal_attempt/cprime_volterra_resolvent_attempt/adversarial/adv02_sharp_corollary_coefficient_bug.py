"""
adv02_sharp_corollary_coefficient_bug.py -- CENTRAL FINDING of this
referee's review. Demonstrates that the target's Sec 3.4 (SHARP)
formula,

    ||K(y,t)||  <=  (1-e^{-h/eps})*(R(z)+eps*sigma(z))  +  eps*e^{-h/eps}

is NOT a universally valid upper bound on the true operator norm
||K(y,t)|| -- it can be, and demonstrably is, VIOLATED (the true norm
exceeds it) in a genuine, non-degenerate parameter regime, even though
Theorem A and Theorem B (the two ingredients it is built from) are BOTH
independently confirmed correct (adv01).

THE EXACT IDENTITY (elementary, re-derived here, and confirmed
numerically to 40-50 digits below):

  Since D(s) >= 0 on [0,h] (Thm A) and D(s) <= 0 for s>h (Thm B),
    K(y,t)[1](x) = int_0^inf D(s) ds
                 = int_0^h D(s) ds  -  int_h^inf |D(s)| ds
  so
    int_0^h D(s) ds  =  K(y,t)[1](x)  +  int_h^inf |D(s)| ds        (EXACT)

  and therefore
    ||K(y,t)||  =  int_0^h D(s) ds  +  int_h^inf |D(s)| ds
                =  K(y,t)[1](x)  +  2 * int_h^inf |D(s)| ds         (EXACT)

Theorem B proves int_h^inf|D(s)|ds <= eps*e^{-h/eps} -- so the CORRECT,
rigorously-justified upper bound coming out of Theorem A + Theorem B is

    ||K(y,t)||  <=  K(y,t)[1](x)  +  2*eps*e^{-h/eps}                 (SHARP, CORRECTED)

with COEFFICIENT 2 on the tail term, not 1. The target's own s04 Part 4 /
ATTEMPT.md Sec 3.4 asserts coefficient 1, with an explicit inline note
claiming to have self-caught and corrected an EARLIER "2*eps" hand
estimate down to "eps" -- i.e. the target's own self-correction
narrative (Sec 7 Issue 3) describes exactly the moment this bug was
introduced, believing it to be a fix. The "2*eps" heuristic they
discarded was, in the specific sense made precise above, actually closer
to the truth than their own "fix".

This script:
  (1) confirms the EXACT identity ||K(y,t)|| = K(y,t)[1](x) + 2*tail_exact
      numerically to 40-50 digits (mpmath) at a specific case,
  (2) confirms Theorem B's own bound (tail_exact <= eps*e^{-h/eps}) still
      holds (Theorem B itself is NOT broken),
  (3) exhibits a CONCRETE (eps,z,h) triple where the target's
      coefficient-1 (SHARP) formula is VIOLATED by the true norm, at
      dps=50 (i.e. not a quadrature-noise artifact),
  (4) confirms the corrected coefficient-2 formula IS a valid bound at
      that same point (and, being a direct algebraic consequence of
      Theorem B alone, is valid unconditionally -- no further search
      needed to establish its validity, only its use here as a sanity
      check).
"""
import mpmath as mp
mp.mp.dps = 50

def D_KAraw_direct(s, h, z, eps):
    upper = min(h, s)
    if upper <= 0:
        return mp.mpf(0)
    f = lambda v: mp.e**(-v/eps) * mp.e**(-(s-v)**2/2 - (s-v)*z)
    return mp.quad(f, [0, upper])

def D_KB(s, h, eps):
    return mp.e**(-s/eps) if (0 <= s <= h) else mp.mpf(0)

def D_full(s, h, z, eps):
    Myv = (1-eps*z)/eps
    return D_KB(s,h,eps) + Myv*D_KAraw_direct(s,h,z,eps)

def R(a):
    f = lambda u: mp.e**(-u**2/2 - u*a)
    return mp.quad(f, [0, mp.inf])

eps = mp.mpf('0.2')
z = mp.mpf('8.0')
h = mp.mpf('0.8')
w = z - 1/eps
print(f"Test point: eps={eps}, z={z}, h={h}  (w=z-1/eps={w})")
print()

print("="*90)
print("Step 1: the EXACT identity ||K(y,t)|| = K(y,t)[1](x) + 2*int_h^inf|D|ds")
print("="*90)
true_norm_unified = mp.quad(lambda s: abs(D_full(s,h,z,eps)),
                             [0, h*mp.mpf('0.5'), h, h+eps, h+3*eps, h+8*eps,
                              h+20*eps, h+50*eps, mp.inf])
pos_piece = mp.quad(lambda s: D_full(s,h,z,eps), [0, h*mp.mpf('0.5'), h])
neg_piece_signed = mp.quad(lambda s: D_full(s,h,z,eps),
                            [h, h+eps, h+3*eps, h+8*eps, h+20*eps, h+50*eps, mp.inf])
tail_exact = -neg_piece_signed
Rz = R(z); sigma_z = 1 - z*Rz
K1_exact_val = (1-mp.e**(-h/eps))*(Rz+eps*sigma_z)

print("int_0^h D(s)ds                          =", mp.nstr(pos_piece, 30))
print("K(y,t)[1](x) exact formula               =", mp.nstr(K1_exact_val, 30))
print("int_h^inf|D(s)|ds (= tail_exact)          =", mp.nstr(tail_exact, 30))
print("K(y,t)[1](x) + tail_exact                 =", mp.nstr(K1_exact_val+tail_exact, 30))
print("  (should equal int_0^h D(s)ds above -- confirms the EXACT identity)")
assert abs((K1_exact_val+tail_exact) - pos_piece) < mp.mpf('1e-25')
print("  CONFIRMED, residual < 1e-25")
print()
print("TRUE ||K(y,t)|| (unified |D(s)| integral) =", mp.nstr(true_norm_unified, 30))
print("K(y,t)[1](x) + 2*tail_exact                =", mp.nstr(K1_exact_val + 2*tail_exact, 30))
assert abs(true_norm_unified - (K1_exact_val + 2*tail_exact)) < mp.mpf('1e-25')
print("  CONFIRMED MATCH -- the exact identity ||K|| = K[1] + 2*tail is verified. PASS")

print()
print("="*90)
print("Step 2: Theorem B's own bound still holds (Theorem B is NOT broken)")
print("="*90)
bound = eps*mp.e**(-h/eps)
print("Theorem B bound eps*e^-h/eps =", mp.nstr(bound, 30))
print("actual tail_exact            =", mp.nstr(tail_exact, 30))
assert tail_exact <= bound
print("tail_exact <= bound: CONFIRMED, Theorem B itself is correct.")

print()
print("="*90)
print("Step 3: the target's coefficient-1 (SHARP) formula IS VIOLATED here")
print("="*90)
SHARP_target = K1_exact_val + 1*bound
SHARP_corrected = K1_exact_val + 2*bound
print("Target's (SHARP), coefficient 1  =", mp.nstr(SHARP_target, 30))
print("TRUE ||K(y,t)||                   =", mp.nstr(true_norm_unified, 30))
print("Corrected (SHARP), coefficient 2 =", mp.nstr(SHARP_corrected, 30))
print()
if true_norm_unified > SHARP_target:
    excess = true_norm_unified - SHARP_target
    print(f">>> VIOLATION CONFIRMED: TRUE exceeds target's (SHARP) by "
          f"{mp.nstr(excess,10)} (relative {mp.nstr(excess/SHARP_target,6)}) <<<")
else:
    print("No violation at this point (unexpected given prior exploration).")
assert true_norm_unified <= SHARP_corrected, "even the corrected coefficient-2 bound failed!"
print("Corrected coefficient-2 bound holds here (as it must, being an exact")
print("algebraic consequence of Theorem B alone, valid unconditionally, not")
print("merely checked at this one point).")

print()
print("="*90)
print("Step 4: broad numerical sweep (mpmath, dps=30) for further violations")
print("="*90)
mp.mp.dps = 30
def D_KAraw_direct30(s, h, z, eps):
    upper = min(h, s)
    if upper <= 0:
        return mp.mpf(0)
    f = lambda v: mp.e**(-v/eps) * mp.e**(-(s-v)**2/2 - (s-v)*z)
    return mp.quad(f, [0, upper])
def D_full30(s, h, z, eps):
    Myv = (1-eps*z)/eps
    dkb = mp.e**(-s/eps) if (0 <= s <= h) else mp.mpf(0)
    return dkb + Myv*D_KAraw_direct30(s,h,z,eps)
def R30(a):
    return mp.quad(lambda u: mp.e**(-u**2/2 - u*a), [0, mp.inf])

n_viol = 0
n_total = 0
worst = (mp.mpf(0), None)
for eps_ in ['0.2','0.3','0.5']:
    eps_v = mp.mpf(eps_)
    for w_ in ['1.0','2.0','3.0','5.0']:
        w_v = mp.mpf(w_)
        z_v = w_v + 1/eps_v
        for hfrac in ['1.0','2.0','3.0','4.0']:
            h_v = mp.mpf(hfrac)*eps_v
            n_total += 1
            tail = mp.quad(lambda s: abs(D_full30(s,h_v,z_v,eps_v)),
                            [h_v, h_v+2*eps_v, h_v+6*eps_v, h_v+20*eps_v, mp.inf])
            bnd = eps_v*mp.e**(-h_v/eps_v)
            Rz_v = R30(z_v); sg = 1-z_v*Rz_v
            K1v = (1-mp.e**(-h_v/eps_v))*(Rz_v+eps_v*sg)
            SHARP1 = K1v+bnd
            TRUEv = K1v+2*tail
            ratio = TRUEv/SHARP1
            if ratio > worst[0]:
                worst = (ratio, (eps_,w_,hfrac))
            if TRUEv > SHARP1*mp.mpf('1.0000001'):
                n_viol += 1
print(f"Tested {n_total} (eps,w,h/eps) triples: {n_viol} violations of the target's")
print(f"coefficient-1 (SHARP) formula found. Worst TRUE/SHARP ratio = "
      f"{mp.nstr(worst[0],6)} at (eps,w,h/eps)={worst[1]}.")
print()
print("CONCLUSION: the target's (SHARP) formula (Sec 3.4) is mathematically")
print("INCORRECT as an unconditional bound -- it requires coefficient 2, not 1,")
print("on the eps*e^{-h/eps} tail term. Theorem A and Theorem B (adv01) remain")
print("correct; the error is specifically in how Sec 3.4 assembles them. See")
print("adv03 for the propagated impact on Sec 4-5's downstream numerics.")
