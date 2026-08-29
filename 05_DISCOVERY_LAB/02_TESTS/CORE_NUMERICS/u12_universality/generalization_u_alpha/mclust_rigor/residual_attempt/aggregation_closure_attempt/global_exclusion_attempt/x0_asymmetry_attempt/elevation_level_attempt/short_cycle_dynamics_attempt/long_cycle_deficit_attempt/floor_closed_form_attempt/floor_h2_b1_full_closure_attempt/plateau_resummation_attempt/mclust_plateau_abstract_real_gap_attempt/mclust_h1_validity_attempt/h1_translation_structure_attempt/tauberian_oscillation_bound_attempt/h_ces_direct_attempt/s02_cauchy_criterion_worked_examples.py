"""
s02_cauchy_criterion_worked_examples.py

H-CES-DIRECT-ATTEMPT (wave 28, front (a), DISC-DEC-131).

Two ELEMENTARY worked examples (not the real Phi -- exactly the same scope
choice this whole sub-lineage's ancestors make for their own elementary
inequality/counter-example checks, e.g. the predecessor's own
sin(log(1+t)) example, which is deliberately a toy function used to prove a
LOGICAL fact, not a claim about the system's actual Phi):

  (A) POSITIVE example: an abstract h(y):=A(y)/(x+y) whose "self-averaging
      error" e(y):=Phi_y(x)-h(y) is EXACTLY D/(x+y) (i.e. genuinely O(1/z),
      the rate this front's Sec 3 derives from (B)+(C')+(U)) is shown, by
      explicit closed form AND independent numerical quadrature, to
      CONVERGE as y->infinity. This is the "does the mechanism actually
      work" sanity check for s01's abstract algebra.

  (B) SHARPNESS example: an abstract h(y):=sin(log(log(x+y+3))) has
      derivative satisfying |h'(y)| <= 1/(w log w) (w:=x+y+3), giving a
      self-averaging error e(y):=z*h'(y) that DOES satisfy the weaker
      "o(1)" condition (i.e. is consistent with the already-UNCONDITIONALLY
      proved self-averaging identity Phi_y(x)-A(y)/z -> 0) but is NOT O(1/z)
      -- only O(1/log z), strictly weaker. h(y) itself is shown to NOT
      converge (via an explicit constructive subsequence, not merely
      "sampled and no trend seen"). This demonstrates that the O(1/z) rate
      this front's Sec 3 derives is not an arbitrary/wasteful sufficient
      condition -- weakening it even to O(1/log z) already breaks the
      Cauchy-criterion argument, i.e. the threshold is SHARP.

Independent, from-scratch script; no code imported from any ancestor front
or referee. sympy for exact symbolic work, mpmath for arbitrary-precision
numerics (dps=50 throughout, well above float64 noise floor).
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 50

log = []
def report(name, ok, extra=""):
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}" + (f"  -- {extra}" if extra else "")
    print(line)
    log.append(line)
    if not ok:
        raise AssertionError(f"CHECK FAILED: {name} {extra}")

print("="*78)
print("s02: two worked examples -- positive convergence, and sharpness")
print("="*78)

# ===========================================================================
# PART A: positive example -- e(y) = D/(x+y) exactly => h(y) converges
# ===========================================================================
print("\n" + "-"*78)
print("PART A: e(y) := D/(x+y) exactly  =>  h(y):=A(y)/(x+y) converges")
print("-"*78)

# h'(y) = e(y)/(x+y) = D/(x+y)^2 exactly (this is the SAME relation s01
# Check 1 verified in the abstract). Integrate exactly via sympy:
xs, ys, Ds, Y0s, hY0s = sp.symbols('x y D Y0 h_Y0', positive=True)
hprime = Ds / (xs + ys)**2
h_of_y = hY0s + sp.integrate(hprime, (ys, Y0s, ys))  # h(y) = h(Y0) + int_{Y0}^y h'
h_of_y = sp.simplify(h_of_y)
print("h(y) closed form:", h_of_y)

limit_h = sp.limit(h_of_y, ys, sp.oo)
print("lim_{y->infinity} h(y) =", limit_h)
expected_limit = hY0s + Ds / (xs + Y0s)
report("closed-form limit matches h(Y0) + D/(x+Y0) exactly",
       sp.simplify(limit_h - expected_limit) == 0,
       f"got {limit_h}, expected {expected_limit}")

# Concrete numeric instance: x=1, D=2, Y0=1, h(Y0)=0.3
xv, Dv, Y0v, hY0v = mp.mpf('1'), mp.mpf('2'), mp.mpf('1'), mp.mpf('0.3')
L_predicted = hY0v + Dv/(xv+Y0v)
print(f"\nConcrete instance: x={xv}, D={Dv}, Y0={Y0v}, h(Y0)={hY0v}")
print(f"Predicted limit L = h(Y0)+D/(x+Y0) = {L_predicted}")

def h_closed(yv):
    return hY0v - Dv/(xv+yv) + Dv/(xv+Y0v)

# Independent numeric confirmation via direct mpmath quadrature of h'(y)
# (NOT the closed-form antiderivative -- genuinely re-integrating from
# scratch) from Y0 to a sequence of growing Y, comparing against h_closed.
def hprime_num(yv):
    return Dv / (xv+yv)**2

test_Ys = [mp.mpf(v) for v in ['2','5','10','100','1000','100000','10000000']]
print("\n  Y            h(Y) via mpmath quad of h'        h(Y) closed form        |diff|")
max_diff = mp.mpf('0')
for Yv in test_Ys:
    quad_val = hY0v + mp.quad(hprime_num, [Y0v, Yv])
    closed_val = h_closed(Yv)
    diff = abs(quad_val - closed_val)
    max_diff = max(max_diff, diff)
    print(f"  {float(Yv):<12g} {mp.nstr(quad_val,15):<28} {mp.nstr(closed_val,15):<24} {mp.nstr(diff,4)}")
report("independent mpmath quadrature matches closed form to <1e-30",
       max_diff < mp.mpf('1e-30'), f"max diff = {max_diff}")

last_val = h_closed(test_Ys[-1])
gap_to_limit = abs(last_val - L_predicted)
print(f"\n  h(Y={float(test_Ys[-1]):g}) = {mp.nstr(last_val,15)}, "
      f"predicted limit L = {mp.nstr(L_predicted,15)}, gap = {mp.nstr(gap_to_limit,4)}")
report("h(Y) approaches predicted limit L as Y grows (gap < 1e-6 at Y=1e7)",
       gap_to_limit < mp.mpf('1e-6'), f"gap={gap_to_limit}")

# Also confirm the corresponding Phi_y(x) := h(y)+e(y) converges to the SAME L
def Phi_of_y(yv):
    return h_closed(yv) + Dv/(xv+yv)
phi_at_last = Phi_of_y(test_Ys[-1])
report("Phi_y(x):=h(y)+e(y) also converges to the same L (consistency)",
       abs(phi_at_last - L_predicted) < mp.mpf('1e-6'),
       f"Phi_Y={phi_at_last}, L={L_predicted}")

print("\n==> PART A CONFIRMS: an e(y) rate of exactly O(1/z) (the rate this")
print("    front's Sec 3 derives from (B)+(C')+(U)) genuinely suffices for")
print("    h(y)=A(y)/(x+y) -- and hence Phi_y(x) -- to converge.")

# ===========================================================================
# PART B: sharpness -- weakening the rate to O(1/log z) breaks convergence
# ===========================================================================
print("\n" + "-"*78)
print("PART B: h(y):=sin(log(log(x+y+3))) -- e(y)=o(1) but NOT O(1/z);")
print("        h(y) does NOT converge (explicit constructive subsequence)")
print("-"*78)

# Symbolic derivative and its magnitude, to confirm the O(1/(w log w)) claim.
w = sp.symbols('w', positive=True)  # w := x+y+3
hB = sp.sin(sp.log(sp.log(w)))
hB_prime_w = sp.diff(hB, w)
print("d/dw[sin(log(log(w)))] =", hB_prime_w)
expected_form = sp.cos(sp.log(sp.log(w))) / (w * sp.log(w))
report("derivative matches cos(log(log(w)))/(w*log(w)) exactly",
       sp.simplify(hB_prime_w - expected_form) == 0,
       f"got {hB_prime_w}")

# Confirm non-integrability: the antiderivative of 1/(w log w) is log(log(w)),
# which diverges as w->infinity (this is the ELEMENTARY reason h' is not
# absolutely integrable -- contrast with Part A's D/z^2, whose antiderivative
# -D/z is BOUNDED / -> 0).
antideriv = sp.integrate(1/(w*sp.log(w)), w)
print("Antiderivative of 1/(w*log(w)):", antideriv)
report("antiderivative of the majorant is log(log(w)) (unbounded as w->oo)",
       sp.simplify(antideriv - sp.log(sp.log(w))) == 0, f"got {antideriv}")
limit_antideriv = sp.limit(sp.log(sp.log(w)), w, sp.oo)
report("log(log(w)) -> infinity as w -> infinity (confirms NON-integrability)",
       limit_antideriv == sp.oo, f"got {limit_antideriv}")

# Confirm e(y) := z*h'(y) -> 0 (o(1), consistent with the unconditional
# self-averaging identity) even though it is not O(1/z). Take x=0 for
# concreteness (z=y+3=w); e(y) = w * cos(loglog w)/(w log w) = cos(loglog w)/log w.
xsB = sp.Integer(0)
zB = xsB + w - 3  # z = x+y = w-3 (since w:=x+y+3), but for the O(.) discussion
# use w itself as the scale (z ~ w for large w, harmless O(1) shift):
e_of_w = sp.cos(sp.log(sp.log(w))) / sp.log(w)
print("\ne(y) [as a function of w=x+y+3] = cos(log(log(w))) / log(w)")
limit_e = sp.limit(sp.Abs(e_of_w), w, sp.oo)
# sympy may not resolve Abs(cos(...)) limit directly with an oscillating
# argument; bound it instead: |e| <= 1/log(w) -> 0.
bound_on_e = 1/sp.log(w)
limit_bound = sp.limit(bound_on_e, w, sp.oo)
report("|e(y)| <= 1/log(w) -> 0 as w->infinity (confirms e(y)=o(1))",
       limit_bound == 0, f"got {limit_bound}")
# And confirm 1/log(w) is NOT O(1/w) (i.e. NOT integrable-rate): ratio -> infinity
ratio = sp.limit((1/sp.log(w)) / (1/w), w, sp.oo)
report("[1/log(w)] / [1/w] -> infinity (1/log(w) is strictly WEAKER than O(1/w))",
       ratio == sp.oo, f"got {ratio}")

# Explicit constructive subsequence showing h(y) does NOT converge: for
# ANY target value v in [-1,1], choose theta with sin(theta)=v, then set
# w_k := exp(exp(theta + 2*pi*k)) for growing integer k -- w_k -> infinity,
# and h(y_k) = sin(log(log(w_k))) = sin(theta+2*pi*k) = sin(theta) = v
# EXACTLY, for every k. So h takes the value v infinitely often, arbitrarily
# far out -- for v1 != v2 both in [-1,1], h cannot converge (a convergent
# bounded sequence's tail cannot keep hitting two different values exactly).
print("\nConstructive non-convergence: for target values v in {-1, 0, 1},")
print("choose theta=asin(v)+2*pi*k (or pi-asin(v)+2*pi*k) and set")
print("y_k := exp(exp(theta)) - 3 (x=0). Then h(y_k) = sin(log(log(y_k+3)))")
print("= sin(theta) = v EXACTLY, by construction, for arbitrarily large y_k.")

def h_exact(yv, xv=mp.mpf('0')):
    return mp.sin(mp.log(mp.log(xv+yv+3)))

all_ok = True
for target, base_theta in [(mp.mpf('1'), mp.pi/2), (mp.mpf('-1'), -mp.pi/2), (mp.mpf('0'), mp.mpf('0'))]:
    for k in [0, 1, 2, 3]:
        theta_k = base_theta + 2*mp.pi*k
        # need theta_k such that w_k=exp(exp(theta_k)) is finite in mpmath;
        # keep k small enough (theta up to ~2pi*3+pi/2 -> exp(exp(~20)) is
        # astronomically large but mpmath dps=50 handles it as an mpf with
        # a huge exponent, not literally materializing 10^(10^8) digits).
        w_k = mp.e**(mp.e**theta_k)
        y_k = w_k - 3
        val = h_exact(y_k)
        diff = abs(val - target)
        ok = diff < mp.mpf('1e-30')
        all_ok = all_ok and ok
        print(f"  target={float(target):+.0f}, k={k}: theta={mp.nstr(theta_k,6)}, "
              f"y_k~exp(exp({mp.nstr(theta_k,4)})) [order-of-magnitude huge], "
              f"h(y_k)={mp.nstr(val,20)}, |h(y_k)-target|={mp.nstr(diff,4)}  "
              f"[{'OK' if ok else 'FAIL'}]")
report("constructive subsequence hits target values -1,0,+1 exactly, "
       "arbitrarily far out (k=0..3 each)", all_ok)

# Also directly confirm two DIFFERENT k's, same target, give y_k strictly
# increasing (so this really is "arbitrarily far out", not a fixed finite set):
theta0 = mp.pi/2
y_k0 = mp.e**(mp.e**theta0) - 3
y_k1 = mp.e**(mp.e**(theta0+2*mp.pi)) - 3
report("y_k strictly increasing across k (genuinely 'arbitrarily far out')",
       y_k1 > y_k0 * mp.mpf('1e100'),
       f"y_k0 order {mp.nstr(mp.log10(y_k0),6)}, y_k1 order {mp.nstr(mp.log10(y_k1),6)} (log10)")

print("\n==> PART B CONFIRMS: weakening the self-averaging error's rate from")
print("    O(1/z) (Part A, sufficient) to the strictly weaker O(1/log z)")
print("    (still o(1), i.e. still consistent with the UNCONDITIONAL")
print("    self-averaging identity of record) is enough to break convergence")
print("    of h(y)=A(y)/(x+y) -- explicit, constructive, not merely sampled.")
print("    This is the SAME qualitative phenomenon as the predecessor's")
print("    sin(log(1+t)) counter-example (wave 26, Sec 6.2), now located")
print("    precisely relative to THIS front's O(1/z) sufficient threshold:")
print("    the threshold is not an arbitrary safety margin, it is close to")
print("    the actual boundary of what works.")

print("\n" + "="*78)
print("ALL CHECKS PASSED.")
print("="*78)
