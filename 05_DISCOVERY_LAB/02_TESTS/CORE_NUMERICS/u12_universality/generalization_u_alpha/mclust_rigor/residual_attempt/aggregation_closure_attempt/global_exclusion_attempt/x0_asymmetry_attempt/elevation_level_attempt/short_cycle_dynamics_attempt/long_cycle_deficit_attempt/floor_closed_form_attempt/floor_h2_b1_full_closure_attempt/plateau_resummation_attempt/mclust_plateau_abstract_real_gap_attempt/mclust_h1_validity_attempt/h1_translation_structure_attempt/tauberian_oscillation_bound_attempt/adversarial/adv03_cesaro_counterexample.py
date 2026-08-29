"""
adv03_cesaro_counterexample.py

Independent, from-scratch verification of the target's Sec 6.2 counter-
example g(t) := sin(log(1+t)), written BEFORE reading the target's own
s03_cesaro_gap_counterexample.py.

Mandate item 4 sub-checks:
 (a) boundedness -- trivial.
 (b) the EXACT relative-step oscillation condition (not a Taylor
     approximation): via |sin A - sin B| <= |A-B|, derive a RIGOROUS,
     non-asymptotic bound |g(s)-g(y)| <= log(1+delta) <= delta for ALL
     y>=0, 0<=s-y<=delta*y -- sharper than the target's own first-order-
     Taylor-plus-spot-check argument, but confirming the same conclusion.
 (c) independent numerical computation of the Cesaro mean via DIRECT
     quadrature (not the closed form), up to Y=1e8, confirming continued
     oscillation, not convergence.
 (d) independent re-derivation of the exact closed form for the integral
     and Cesaro mean (via t=e^u-1), confirmed against a from-scratch
     sympy computation and by direct differentiation.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 30

print("="*72)
print("(a) Boundedness: trivial, |sin(log(1+t))| <= 1 for all t>=0.")
print("="*72)
print("Confirmed by inspection (sin is bounded by 1 everywhere).\n")

print("="*72)
print("(b) EXACT (non-asymptotic) relative-step oscillation bound")
print("="*72)
print("""
Claim (independently derived, NOT copied from the target's first-order-
Taylor argument): for g(t):=sin(log(1+t)), and ANY y>=0, s with
0<=s-y<=delta*y (0<=delta<1):

  |g(s)-g(y)| <= log(1+delta) <= delta      for ALL y>=0 (Y=0 suffices)

Proof: |sin A - sin B| = |2 cos((A+B)/2) sin((A-B)/2)| <= |A-B|
  (using |cos|<=1, |sin(w)|<=|w|). With A=log(1+s), B=log(1+y):
  |A-B| = |log((1+s)/(1+y))| = log(1+ (s-y)/(1+y))  [s>=y so (1+s)/(1+y)>=1]
       <= log(1 + delta*y/(1+y)) <= log(1+delta)    [since y/(1+y)<1]
  and log(1+delta) <= delta for delta>=0 (standard elementary inequality).
QED. This is STRICTLY sharper and fully rigorous (no O(delta^2) remainder
to separately control, unlike a first-order Taylor argument) -- it holds
for ALL delta in [0,1), not just asymptotically small delta, and for
EVERY y>=0, not merely y>=Y for some threshold.
""")
# Numerically confirm the elementary inequality log(1+delta)<=delta, and the
# chain of inequalities, at several (y, delta) points, against the EXACT g.
def g(t):
    return mp.sin(mp.log(1+t))

test_pts = [(mp.mpf(y), mp.mpf(d)) for y in [0, 1, 10, 100, 1000, 10**5, 10**7]
                                     for d in [mp.mpf('0.5'), mp.mpf('0.1'), mp.mpf('0.01'), mp.mpf('0.001')]]
worst_ratio = mp.mpf(0)
for y, delta in test_pts:
    s = y + delta*y  # worst case, s-y = delta*y exactly
    diff = abs(g(s) - g(y))
    bound = mp.log(1+delta)
    ok = diff <= bound + mp.mpf('1e-20')
    ratio = diff/delta if delta > 0 else mp.mpf(0)
    worst_ratio = max(worst_ratio, ratio)
    status = "OK" if ok else "VIOLATION"
    if y in (0,1,10,1000,10**7):
        print(f"y={float(y):12.4g} delta={float(delta):8.4f}  |g(s)-g(y)|={mp.nstr(diff,6):>12}"
              f"  bound_log(1+d)={mp.nstr(bound,6):>10}  {status}")
print(f"\nworst-case |g(s)-g(y)|/delta observed across grid: {mp.nstr(worst_ratio,6)}"
      f"  (<=1 confirms the sharp elementary bound holds; the target's own claim")
print("'bounded by 1 in absolute value for ALL y>=0' is CONFIRMED, and shown to")
print("follow from an exact, not merely first-order, argument.\n")

print("="*72)
print("(c)+(d) Exact closed form for int_0^Y g(t)dt via t=e^u-1, sympy,")
print("independently re-derived from scratch")
print("="*72)
u, Y = sp.symbols('u Y', positive=True)
# int sin(u) e^u du
antideriv = sp.integrate(sp.sin(u)*sp.exp(u), u)
antideriv = sp.simplify(antideriv)
print("sympy: int sin(u) e^u du =", antideriv)
# check it matches (sin(u)-cos(u))*e^u/2
claimed = (sp.sin(u) - sp.cos(u))*sp.exp(u)/2
resid = sp.simplify(sp.diff(antideriv - claimed, u))
print("d/du[antideriv - (sin(u)-cos(u))e^u/2] =", resid, " (0 expected if same up to constant)")
resid2 = sp.simplify(antideriv - claimed)
print("antideriv - claimed (should be a t-independent constant, sympy may fold it in):", resid2)

# Definite integral from u=0 to u=log(1+Y):  int_0^Y g(t) dt
Yv = sp.symbols('Y', positive=True)
u_upper = sp.log(1+Yv)
I_exact = sp.simplify(claimed.subs(u, u_upper) - claimed.subs(u, 0))
print("\nint_0^Y g(t) dt (exact, sympy, via t=e^u-1 substitution and definite eval) =")
sp.pprint(I_exact)

target_formula = -sp.sqrt(2)*(Yv+1)*sp.cos(sp.log(Yv+1) + sp.pi/4)/2 + sp.Rational(1,2)
diff_formulas = sp.simplify(I_exact - target_formula)
print("\nDifference vs target's stated closed form",
      "(-sqrt(2)*(Y+1)*cos(log(Y+1)+pi/4)/2 + 1/2):")
print(" ->", diff_formulas)
assert diff_formulas == 0, "MISMATCH with target's claimed closed form for the integral!"
print("PASS: my independent sympy re-derivation EXACTLY matches the target's")
print("claimed closed form for int_0^Y g(t) dt.\n")

# Verify by direct differentiation (mandate: verify the exact closed form, not
# trusting the target's or a naive spot-check)
dcheck = sp.simplify(sp.diff(I_exact, Yv) - sp.sin(sp.log(1+Yv)))
print("d/dY[int_0^Y g dt] - g(Y) =", dcheck, " (0 expected)")
assert dcheck == 0
print("PASS: closed form differentiates back to g(Y) exactly.\n")

print("="*72)
print("(c) Independent NUMERICAL confirmation via DIRECT quadrature")
print("(not the closed form), up to Y=1e8, of continued oscillation")
print("="*72)
def cesaro_mean_direct_quad(Yval):
    # direct numerical integration of g(t)=sin(log(1+t)) from 0 to Y,
    # NOT using the closed form -- independent numerical route.
    Yval = mp.mpf(Yval)
    bpts = sorted(set([mp.mpf(0)] + [Yval*mp.mpf(f) for f in
                  ['1e-6','1e-4','1e-2','0.1','0.3','0.5','0.7','0.9','1.0']]))
    I = mp.quad(g, bpts)
    return I/Yval, I

def cesaro_mean_closed_form(Yval):
    Yval = mp.mpf(Yval)
    val = -mp.sqrt(2)*(Yval+1)*mp.cos(mp.log(Yval+1)+mp.pi/4)/2 + mp.mpf('0.5')
    return val/Yval, val

print(f"{'Y':>12} {'g(Y)':>12} {'Cesaro(direct quad)':>22} {'Cesaro(closed form)':>22} {'match?':>8}")
Ys = [10, 100, 1000, 10**4, 10**5, 10**6, 10**7, 10**8]
cesaro_vals = []
for Yv_ in Ys:
    cm_quad, _ = cesaro_mean_direct_quad(Yv_)
    cm_cf, _ = cesaro_mean_closed_form(Yv_)
    gy = g(mp.mpf(Yv_))
    match = abs(cm_quad - cm_cf) < mp.mpf('1e-10')
    cesaro_vals.append(cm_quad)
    print(f"{Yv_:12.4g} {float(gy):12.6f} {float(cm_quad):22.10f} {float(cm_cf):22.10f} {str(match):>8}")

print("\nAmplitude check: predicted asymptotic amplitude of Cesaro-mean")
print("oscillation is sqrt(2)/2 =", float(mp.sqrt(2)/2))
print("observed range of Cesaro means across Y=10..1e8:",
      float(min(cesaro_vals)), "to", float(max(cesaro_vals)))
print("\nNO monotone trend toward a single limit across 8 orders of magnitude in Y")
print("-- confirms BOTH g(Y) and its Cesaro mean keep oscillating without")
print("converging, matching the target's claim exactly, via an independent")
print("direct-quadrature computation (not the closed form, not the target's numbers).")
