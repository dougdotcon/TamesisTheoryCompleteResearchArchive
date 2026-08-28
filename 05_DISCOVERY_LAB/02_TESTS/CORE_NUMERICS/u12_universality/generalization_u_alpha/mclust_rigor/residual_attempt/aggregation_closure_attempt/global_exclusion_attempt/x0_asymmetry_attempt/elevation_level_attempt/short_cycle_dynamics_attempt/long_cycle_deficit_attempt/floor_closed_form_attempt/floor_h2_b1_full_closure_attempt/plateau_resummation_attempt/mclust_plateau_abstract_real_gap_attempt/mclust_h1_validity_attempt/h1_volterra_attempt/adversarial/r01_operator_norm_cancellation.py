"""
ADVERSARIAL CHECK 1 -- re-derive the operator norm of M_y o K_A^raw(y,t) FROM
SCRATCH via a pointwise (not submultiplicative) bound, to test whether the
document's Sec 4.4 claim ("the full kernel's boundedness hinges entirely on
||M_y||, which grows unboundedly / linearly in y") survives a more careful
analysis that exploits the exact shift-cancellation x'+w = x+y.

Definitions (from ATTEMPT.md Sec 4.1, transcribed independently, not from
any .py file of the target front or any ancestor):
  R(z) := sqrt(pi/2) * erfcx(z/sqrt(2))
  T_w f(x) := int_0^inf e^{-u^2/2 - u(x+w)} f(x+u) du
  S_v f(x) := f(x+v)
  K_A^raw(y,t) f (x) := int_t^y e^{-(y-w)/eps} (S_{y-w} T_w f)(x) dw
  M_y f (x) := [(1-eps(x+y))/eps] * f(x)

Step 1: (S_{y-w} T_w f)(x) = (T_w f)(x+y-w)
       = int_0^inf e^{-u^2/2 - u((x+y-w)+w)} f(x+y-w+u) du
       = int_0^inf e^{-u^2/2 - u(x+y)} f(x+y-w+u) du        <-- exponent has
         NO w-dependence: (x+y-w)+w = x+y exactly.

Step 2: |(S_{y-w}T_w f)(x)| <= ||f||_inf * R(x+y)   (independent of w, t !)

Step 3: |(K_A^raw(y,t) f)(x)| <= ||f||_inf * R(x+y) * int_t^y e^{-(y-w)/eps} dw
                              <= ||f||_inf * R(x+y) * eps

Step 4: |(M_y K_A^raw(y,t) f)(x)| <= |1/eps - x - y| * eps * R(x+y)
                                   = |1 - eps*(x+y)| * R(x+y)
        Let z := x+y (z ranges over [y, infinity) as x ranges over [0,infinity)).
        Define h_eps(z) := |1 - eps*z| * R(z).

Claim under test: is h_eps(z) UNIFORMLY BOUNDED over z in [0,infinity),
for fixed eps -- i.e. does the pointwise bound show M_y o K_A^raw(y,t) is
actually a BOUNDED operator on the full unrestricted x-domain, contradicting
ATTEMPT.md Sec 4.4's claim that boundedness fails there and that the
obstruction "hinges entirely" on the unbounded ||M_y||?

This script computes h_eps(z) at a fine grid + finds its sup numerically,
for several eps, using an independently-written erfcx (mpmath's built-in,
NOT reusing any of the front's own code, per the mandate's "no .py read"
restriction applied here to my own construction: this is FRESH code).
"""
import mpmath as mp

mp.mp.dps = 50

def R(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2) * mp.erfc(z/mp.sqrt(2)) * mp.e**(z*z/2)
    # erfcx(z) = e^{z^2} erfc(z); here argument is z/sqrt2 so erfcx(z/sqrt2)=e^{z^2/2}erfc(z/sqrt2)

def R_via_integral(z):
    # independent check: R(z) = int_0^inf e^{-u^2/2 - u z} du
    f = lambda u: mp.e**(-u*u/2 - u*z)
    return mp.quad(f, [0, mp.inf])

# sanity: R(0) should be sqrt(pi/2)
print("R(0) =", R(0), " sqrt(pi/2)=", mp.sqrt(mp.pi/2))
print("R(0) via integral =", R_via_integral(0))
print("R(2) via closed form:", R(2), " via integral:", R_via_integral(2))
print()

def h(z, eps):
    z = mp.mpf(z); eps = mp.mpf(eps)
    return abs(1 - eps*z) * R(z)

for eps in [mp.mpf('0.1'), mp.mpf('0.0316227766'), mp.mpf('0.01'), mp.mpf('1')]:
    print(f"=== eps = {eps} (c ~ {1/eps**2}) ===")
    zs = [mp.mpf(v) for v in
          [0, 0.001, 0.01, 0.1, 0.5, 1, 1/eps*0.5, 1/eps*0.9, 1/eps, 1/eps*1.1,
           1/eps*2, 1/eps*5, 1/eps*10, 1/eps*50, 1/eps*100, 1/eps*1000]]
    vals = [(z, h(z, eps)) for z in zs]
    for z, v in vals:
        print(f"  z={float(z):>14.6f}   h(z)={float(v):.10f}")
    # find approx sup via fine scan + a local optimizer near z=0 and large z
    fine_zs = [mp.mpf(i)/1000 * 1/eps * 3 for i in range(0, 3001)]
    fine_vals = [h(z, eps) for z in fine_zs]
    mx = max(fine_vals)
    idx = fine_vals.index(mx)
    print(f"  --> numeric sup over fine grid [0, 3/eps]: {float(mx):.10f} at z={float(fine_zs[idx]):.6f}")
    print(f"  --> h(0) = sqrt(pi/2) = {float(mp.sqrt(mp.pi/2)):.10f}  (eps-independent)")
    print(f"  --> h(z) as z->inf tends to eps = {float(eps):.10f}")
    print()
