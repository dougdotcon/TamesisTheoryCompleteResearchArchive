"""
adv02_kernel_uniformity_mpmath.py

Independent, from-scratch mpmath re-implementation of the RAW kernel
definitions (K_A^raw, K_B, M_y -- as cited in Sec 0 of both the target
ATTEMPT.md and its predecessor h1_translation_structure_attempt/ATTEMPT.md),
written without opening any of the target's own .py scripts.

Purpose:
  (a) Sanity check against the predecessor's own published Sec 5.4 value
      (x=0, eps=0.1, f=1/(1+x), h=y/2, y=10: published z*K(y,t)f(0) =
      0.9156333394) -- confirms this independent implementation is correct
      before trusting anything new.
  (b) Reproduce the target's s02b combined transition+large-h sweep
      (eps=5, z=1000 i.e. x=0,y=1000, h/y from 0.0002 to 0.99), checking
      z^2*err stays BOUNDED with no blowup -- the numerical support claimed
      for hypothesis (U) in the "distant past" (h/y -> 1) regime no
      ancestor front tested.

De-stiffening: inner integral via substitution u = v/z (so the sharp
e^{-uz} peak becomes an O(1) integrand in v); outer h'-integral given
explicit breakpoints at multiples of eps (where the e^{-h'/eps} weight
decays), following the same discipline this lineage's fronts and referees
have repeatedly needed to avoid naive-quadrature failures at large z.
"""
import mpmath as mp

mp.mp.dps = 30

def f_rational(xv):
    return 1/(1+xv)

def f_exp(xv):
    return mp.e**(-xv/3)

def theta(hprime, z, x, f):
    """Theta_{h'}(z) = int_0^inf e^{-u^2/2 - u z} f(x+h'+u) du, via u=v/z."""
    def integrand(v):
        u = v/z
        return mp.e**(-u**2/2 - v) * f(x + hprime + u) / z
    # breakpoints in v (dimensionless); mass concentrated at v=O(1)
    bpts = [0, mp.mpf('0.5'), 2, 5, 15, 40, 80]
    return mp.quad(integrand, bpts)

def K_A_raw(y, t, x, eps, f):
    """K_A^raw(y,t) f(x), single-integral reduced form:
       int_0^h e^{-h'/eps} Theta_{h'}(z) dh',  z=x+y, h=y-t."""
    z = x + y
    h = y - t
    if h <= 0:
        return mp.mpf(0)
    def outer(hp):
        return mp.e**(-hp/eps) * theta(hp, z, x, f)
    # breakpoints at multiples of eps, clipped to h
    cand = [eps/10, eps/2, eps, 2*eps, 5*eps, 10*eps, 25*eps, 50*eps]
    bpts = sorted(set([mp.mpf(0)] + [c for c in cand if c < h] + [h]))
    return mp.quad(outer, bpts)

def K_B(h, x, eps, f):
    if h <= 0:
        return mp.mpf(0)
    def integrand(v):
        return mp.e**(-v/eps) * f(x + v)
    cand = [eps/10, eps/2, eps, 2*eps, 5*eps, 10*eps, 25*eps, 50*eps]
    bpts = sorted(set([mp.mpf(0)] + [c for c in cand if c < h] + [h]))
    return mp.quad(integrand, bpts)

def M_y_val(z, eps):
    return (1 - eps*z)/eps

def K_full(y, t, x, eps, f):
    z = x + y
    h = y - t
    A = K_A_raw(y, t, x, eps, f)
    return M_y_val(z, eps)*A + K_B(h, x, eps, f)

def closed_form(y, t, x, eps, f):
    z = x + y
    h = y - t
    return (f(x) - mp.e**(-h/eps)*f(x+h)) / z

# ---------------------------------------------------------------------
print("="*72)
print("PART 1: sanity check against predecessor's published Sec 5.4 value")
print("x=0, eps=0.1, f=1/(1+x), h=y/2, y=10  =>  published z*K(y,t)f(0)=0.9156333394")
print("="*72)
x = mp.mpf(0); eps = mp.mpf('0.1'); y = mp.mpf(10); h = y/2; t = y - h
Kval = K_full(y, t, x, eps, f_rational)
z = x + y
print("This independent implementation: z*K(y,t)f(0) =", z*Kval)
print("Published (h1_translation_structure_attempt Sec 5.4):  0.9156333394")
diff = abs(z*Kval - mp.mpf('0.9156333394'))
print("abs diff =", diff)
assert diff < mp.mpf('1e-8'), "FAILS sanity cross-check!"
print("PASS -- independent implementation confirmed correct.\n")

# ---------------------------------------------------------------------
print("="*72)
print("PART 2: reproduce s02b regime -- eps=5, z=1000 (x=0,y=1000),")
print("h/y ratio sweep 0.0002 -> 0.99, checking z^2*err stays bounded")
print("="*72)
eps2 = mp.mpf(5)
x2 = mp.mpf(0)
y2 = mp.mpf(1000)
z2 = x2 + y2
ratios = [mp.mpf(r) for r in
          ['0.0002','0.001','0.005','0.01','0.02','0.05','0.1','0.3','0.5','0.7','0.9','0.99']]

results = []
for r in ratios:
    h = r*y2
    t = y2 - h
    Kv = K_full(y2, t, x2, eps2, f_rational)
    cf = closed_form(y2, t, x2, eps2, f_rational)
    err = Kv - cf
    z2err = z2**2 * err
    results.append((r, h/eps2, z2err))
    print(f"h/y={float(r):8.4f}  h/eps={float(h/eps2):8.3f}   z^2*err = {mp.nstr(z2err, 6)}")

vals = [abs(v[2]) for v in results]
print("\nmax|z^2*err| =", mp.nstr(max(vals), 6))
print("min|z^2*err| =", mp.nstr(min(vals), 6))
print("\nTarget's claimed table (Sec 4.2): max|z^2*err|=0.493, values -0.154 .. +0.493,")
print("bounded and smoothly varying through the entire transition, no divergence.")

# ---------------------------------------------------------------------
print("="*72)
print("PART 3: spot check x=3 (s02c regime) -- eps=0.1, z in {200,1000},")
print("ratios {0.1,0.5,0.9}")
print("="*72)
eps3 = mp.mpf('0.1')
x3 = mp.mpf(3)
for zt in [mp.mpf(200), mp.mpf(1000)]:
    y3 = zt - x3
    for r in [mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.9')]:
        h = r*y3
        t = y3 - h
        Kv = K_full(y3, t, x3, eps3, f_rational)
        cf = closed_form(y3, t, x3, eps3, f_rational)
        err = Kv - cf
        z2err = zt**2 * err
        print(f"z={float(zt):6.0f} h/y={float(r):5.2f}  z^2*err = {mp.nstr(z2err,6)}")
print("\nTarget's claimed table (Sec 4.3): z^2*err approx -0.039 at z=200, -0.038 at z=1000, constant across ratios.")
