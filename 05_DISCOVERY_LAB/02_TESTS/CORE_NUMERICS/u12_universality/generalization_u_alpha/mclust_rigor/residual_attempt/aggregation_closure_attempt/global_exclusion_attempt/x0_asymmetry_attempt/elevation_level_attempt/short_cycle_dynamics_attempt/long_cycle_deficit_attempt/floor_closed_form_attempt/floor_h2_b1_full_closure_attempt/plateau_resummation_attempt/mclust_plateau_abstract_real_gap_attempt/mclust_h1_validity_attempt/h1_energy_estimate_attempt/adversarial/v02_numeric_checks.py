"""
v02_numeric_checks.py
----------------------
Independent, from-scratch mpmath high-precision numerical verification of:
  (E) the shift identity R(z) := int_0^inf e^{-u^2/2-uz} du = sqrt(pi/2)*erfcx(z/sqrt2)
  (F2) the bound R(z) <= 1/z, z>0
  (G) the TRUE tightness regime of the target's Sec 8.2 Lipschitz-<=1 claim:
      target states "essentially TIGHT (saturated as x->0)". We compute
      y*R(x+y) directly (the actual quantity being bounded, before the
      further R(z)<=1/z relaxation) over a grid of (x,y) to determine
      whether saturation toward 1 really happens as x->0 (fixed y), or
      only as y->inf (any fixed x, including x=0) -- own investigation,
      not present in the target document.
No .py file from this front's lineage was read. dps=50 throughout.
"""
import mpmath as mp

mp.mp.dps = 50

def R(z):
    """R(z) = int_0^inf e^{-u^2/2-uz} du, via mpmath quad -- brute numeric route."""
    f = lambda u: mp.e**(-u**2/2 - u*z)
    return mp.quad(f, [0, mp.inf])

def R_closed(z):
    """Claimed closed form sqrt(pi/2)*erfcx(z/sqrt2)."""
    w = z/mp.sqrt(2)
    erfcx = mp.e**(w**2) * mp.erfc(w)
    return mp.sqrt(mp.pi/2) * erfcx

print("="*78)
print("E. Shift identity numeric check: direct quadrature vs sqrt(pi/2)*erfcx(z/sqrt2)")
print("="*78)
zs = [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('1'), mp.mpf('2'), mp.mpf('5'),
      mp.mpf('10'), mp.mpf('20'), mp.mpf('50')]
for z in zs:
    a = R(z)
    b = R_closed(z)
    reldiff = abs(a-b)/abs(b) if b != 0 else abs(a-b)
    print(f"  z={float(z):6.2f}  quad={mp.nstr(a,20)}  closed={mp.nstr(b,20)}  reldiff={mp.nstr(reldiff,6)}")

print()
print("="*78)
print("F2. Numeric check R(z) <= 1/z for z>0")
print("="*78)
all_pass = True
for z in zs:
    Rz = R_closed(z)
    bound = 1/z
    ok = Rz <= bound
    all_pass = all_pass and ok
    print(f"  z={float(z):6.2f}  R(z)={mp.nstr(Rz,15)}  1/z={mp.nstr(bound,15)}  R(z)<=1/z: {ok}   margin={mp.nstr(bound-Rz,6)}")
print("ALL PASS" if all_pass else "SOME FAILED", "(R(z)<=1/z, z>0)")

print()
print("="*78)
print("G. Tightness regime investigation for Sec 8.2's Lipschitz<=1 claim")
print("   Actual bounded quantity is y*R(x+y) (the Lipschitz ratio's own")
print("   sup, BEFORE the further relaxation R(z)<=1/z to get y/(x+y)).")
print("="*78)

print("\nG1. y*R(y) [i.e. x=0] as y grows -- does it approach 1?")
ys = [mp.mpf(v) for v in ['0.1','0.5','1','2','5','10','20','50','100','500','1000']]
prev = None
for yv in ys:
    val = yv * R_closed(yv)
    trend = "" if prev is None else ("increasing" if val>prev else "decreasing")
    print(f"  y={float(yv):8.2f}   y*R(y) = {mp.nstr(val,15)}   1-y*R(y)={mp.nstr(1-val,8)}  {trend}")
    prev = val

print("\nG2. For FIXED, moderate y (y=1), does y*R(x+y) approach 1 as x->0+ ?")
print("    (this is the regime the target's text literally cites: 'x->0, any fixed y>0')")
y_fixed = mp.mpf('1')
xs = [mp.mpf(v) for v in ['2','1','0.5','0.2','0.1','0.05','0.01','0.001','0']]
for xv in xs:
    val = y_fixed * R_closed(xv + y_fixed)
    print(f"  x={float(xv):8.3f}  y*R(x+y) = {mp.nstr(val,15)}   (target claims this -> 1 as x->0)")
print(f"  ==> At y=1 fixed, even at x=0 exactly, y*R(y)={mp.nstr(y_fixed*R_closed(y_fixed),10)}, NOT close to 1.")
print(f"      The quantity does NOT saturate toward 1 merely by sending x->0 at fixed,")
print(f"      moderate y. (Monotonic decrease in x is visible above, consistent with R")
print(f"      being a decreasing function -- so the SUP over x of y*R(x+y), for fixed y,")
print(f"      IS attained at x=0, but that value itself is far from 1 unless y is ALSO large.)")

print("\nG3. Repeat G2 at a LARGE fixed y (y=100) -- does saturation appear only here?")
y_fixed2 = mp.mpf('100')
for xv in xs:
    val = y_fixed2 * R_closed(xv + y_fixed2)
    print(f"  x={float(xv):8.3f}  y*R(x+y) = {mp.nstr(val,15)}")
print(f"  ==> At y=100 (large), y*R(x+y) is already close to 1 for ALL tested x (including x=0),")
print(f"      confirming saturation toward 1 is driven by y->inf (the SUM x+y->inf), not by x->0.")

print("\nG4. Direct evaluation of sup_x y*R(x+y) at fixed y (monotonicity check):")
print("    R is a strictly decreasing function of its argument (R'=zR-1<0 whenever zR<1,")
print("    true since R(z)<=1/z<... -- confirmed numerically: R(x+y) decreases as x increases")
print("    at fixed y, so y*R(x+y) is maximized at x=0 for EVERY fixed y -- verified above,")
print("    G2/G3 both show monotonic decrease in x).")

print()
print("="*78)
print("CONCLUSION (own finding, Part G):")
print("="*78)
print("""
The quantity actually being bounded in Sec8.2 (y*R(x+y), before the further
relaxation to y/(x+y) via R(z)<=1/z) is DECREASING in x for every fixed y
(confirmed G2/G3), so its supremum over x IS attained at x=0 for each fixed
y -- but that supremum value, y*R(y), is close to 1 ONLY when y itself is
large (G1: y*R(y) -> 1 as y->infinity; at y=1, y*R(y) is only ~0.66, far
from 1). Genuine saturation of the TRUE Lipschitz ratio toward 1 therefore
requires y -> infinity (with x fixed, e.g. x=0) -- NOT "x->0" for an
arbitrary FIXED, finite y, as the target's Sec8.2 parenthetical literally
states ("essentially TIGHT (saturated as x->0), y/(x+y)->1 as x->0, any
fixed y>0"). That parenthetical is a true statement about the FURTHER-
RELAXED bound y/(x+y) (which indeed ->1 as x->0 for ANY fixed y, since
R(z)<=1/z is dropped) but is not by itself evidence that the operator's
TRUE norm approaches 1 -- the true quantity y*R(x+y) requires the SUM
x+y to be large, i.e. y->infinity is the operative regime, with x->0
being at most a co-incidental/optimal choice of x at each fixed y, not
the mechanism producing near-1 values.  The document's overall CONCLUSION
(Lipschitz constant is exactly 1, sup not attained, no strict contraction
by this bounding route) remains CORRECT -- confirmed independently here,
since sup_{x,y} y*R(x+y) = sup_z z*R(z) = 1 (approached, not attained, as
z=x+y->infinity) -- but the specific justification offered for "tightness"
in the text names the wrong asymptotic regime.
""")
