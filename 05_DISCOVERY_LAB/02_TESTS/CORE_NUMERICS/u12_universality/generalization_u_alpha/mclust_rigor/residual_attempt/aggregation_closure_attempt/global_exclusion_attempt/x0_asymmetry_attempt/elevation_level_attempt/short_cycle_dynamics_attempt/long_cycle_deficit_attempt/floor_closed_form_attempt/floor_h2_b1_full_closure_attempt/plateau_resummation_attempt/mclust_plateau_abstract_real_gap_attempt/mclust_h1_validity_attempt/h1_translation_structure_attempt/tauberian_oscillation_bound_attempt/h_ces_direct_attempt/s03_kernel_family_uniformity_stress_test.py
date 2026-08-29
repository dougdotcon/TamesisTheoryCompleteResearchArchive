"""
s03_kernel_family_uniformity_stress_test.py

H-CES-DIRECT-ATTEMPT (wave 28, front (a), DISC-DEC-131).

A FRESH, from-scratch mpmath re-implementation of the raw kernel
K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t), via the single-integral reduction of
K_A^raw (an identity independently re-derived and numerically cross-checked
TWICE already in this lineage's record -- h1_translation_structure_attempt
Sec 2.4, and its referee's adv01 Check 3 -- so re-using it as a cited,
derived FORMULA, re-implemented here from scratch, is legitimate and not
circular; it is NOT the closed-form ASYMPTOTIC this front's own argument is
trying to justify, only an exact change of variables on the RAW operator
definitions).

Sanity check first (mandatory discipline in this sub-lineage): reproduce
h1_translation_structure_attempt's own published Sec 5.4 cross-check value
BEFORE trusting anything new.

NEW test, not run by any ancestor front: hypothesis (U) as it is actually
NEEDED by this front's Sec 3 argument requires the O(1/z^2) closed-form
remainder to be uniform not just in h/y (tested by the predecessor, three
sweeps) but ALSO uniform as the test function f ranges over a FAMILY sharing
a common sup-norm and Lipschitz bound -- simulating how {Phi_t}_{t in [0,y]}
would need to behave under hypothesis (C') (Lipschitz regularity UNIFORM in
t). All three ancestor (U)-tests (s02/s02b/s02c and their referee
reproductions) used a SINGLE FIXED f per sweep; none tested whether the
remainder constant stays bounded as f itself varies within a Lipschitz-
bounded family. This script runs that 2D grid (h/y ratio x family member)
test for the first time in this lineage's record.

Definitions (restated, cited, not re-derived -- from h1_translation_
structure_attempt Sec 0 and Sec 2.4, quoted verbatim in this front's own
ATTEMPT.md Sec 0):
  K_A^raw(y,t) f(x) = int_0^h e^{-h'/eps} Theta_{h'}(z) dh',  h:=y-t, z:=x+y
    Theta_{h'}(z) = int_0^infinity e^{-u^2/2-uz} f(x+h'+u) du
  K_B(h) f(x)  = int_0^h e^{-v/eps} f(x+v) dv
  M_y f(x)     = [(1-eps*(x+y))/eps] * f(x)
  K(y,t) f(x)  = M_y[K_A^raw(y,t)f](x) + K_B(y-t)f(x)
  Closed form:  K(y,t)f(x) ~ [f(x)-e^{-h/eps}f(x+h)]/z + O(1/z^2)

De-stiffening (established methodology in this sub-lineage, re-implemented
fresh here, not copied): substitute u=v/z in Theta_{h'}'s inner integral so
the dominant decay (e^{-v}) is O(1) in scale regardless of z; use explicit
breakpoints at multiples of eps for the outer h'-integral (its own decay
scale) rather than naive quad(0,h).
"""
import time
import mpmath as mp

mp.mp.dps = 15

log = []
def report(name, ok, extra=""):
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {name}" + (f"  -- {extra}" if extra else "")
    print(line)
    log.append(line)
    if not ok:
        raise AssertionError(f"CHECK FAILED: {name} {extra}")


def theta_hprime(hp, z, f, x):
    """Theta_{h'}(z) via the de-stiffened substitution u=v/z."""
    def integrand(v):
        return mp.e**(-v**2/(2*z**2) - v) * f(x + hp + v/z)
    return (mp.mpf(1)/z) * mp.quad(integrand, [0, 2, 8, 25, mp.inf])


def _breakpoints(h, eps, cap=12):
    """GEOMETRIC breakpoints spanning the e^{-h'/eps} decay scale, capped at
    a SMALL fixed count (`cap`) regardless of how large h/eps is -- unlike a
    linear-in-h'/eps breakpoint list (which would need O(h/eps) points and
    was the SELF-CAUGHT PERFORMANCE ISSUE in this script's first version,
    see ATTEMPT.md "Self-caught issues": a linear breakpoint list at every
    eps took 38s for a SINGLE kernel evaluation at h/eps=50, which would
    have made the planned 36-evaluation grid (up to h/eps~196) infeasible.
    Since the integrand e^{-h'/eps}*Theta_{h'}(z) is smooth (no
    singularities) on [0,h], geometric breakpoints at 0, eps/4, eps,
    2*eps, 4*eps, ... give mp.quad's adaptive Gauss-Legendre enough
    resolution near h'=0 (where the weight is largest) while still capping
    the total point count at O(log2(h/eps)), independent of h/eps's actual
    size. Re-validated against the published sanity-check value below
    after this fix (Sec 4 numerical verification, ATTEMPT.md)."""
    bps = [mp.mpf(0)]
    cur = eps/4
    while cur < h and len(bps) < cap:
        bps.append(mp.mpf(cur))
        cur *= 2
    if bps[-1] < h:
        bps.append(mp.mpf(h))
    return bps


def K_A_raw(y, t, x, eps, f):
    h = y - t
    z = x + y
    if h <= 0:
        return mp.mpf(0)
    bps = _breakpoints(h, eps)
    def integrand(hp):
        return mp.e**(-hp/eps) * theta_hprime(hp, z, f, x)
    return mp.quad(integrand, bps)


def K_B(h, x, eps, f):
    if h <= 0:
        return mp.mpf(0)
    bps = _breakpoints(h, eps)
    def integrand(v):
        return mp.e**(-v/eps) * f(x+v)
    return mp.quad(integrand, bps)


def M_y_coeff(x, y, eps):
    return (1 - eps*(x+y))/eps


def K_full(y, t, x, eps, f):
    h = y - t
    return M_y_coeff(x, y, eps)*K_A_raw(y, t, x, eps, f) + K_B(h, x, eps, f)


def closed_form(y, t, x, eps, f):
    h = y - t
    z = x + y
    return (f(x) - mp.e**(-h/eps)*f(x+h)) / z


print("="*78)
print("s03: fresh raw-kernel implementation + family-uniformity stress test")
print("="*78)

# ---------------------------------------------------------------------------
# Sanity check: reproduce h1_translation_structure_attempt's published
# Sec 5.4 cross-check value BEFORE trusting anything new.
#   x=0, eps=0.1, f=1/(1+x), h=y/2, y=10  =>  published z*K(y,t)f(0) = 0.9156333394
# ---------------------------------------------------------------------------
print("\n--- Sanity check against published Sec 5.4 value ---")
t0 = time.time()
x_s, eps_s, y_s = mp.mpf(0), mp.mpf('0.1'), mp.mpf(10)
h_s = y_s/2
t_s = y_s - h_s
f_s = lambda u: 1/(1+u)
z_s = x_s + y_s
Kval = K_full(y_s, t_s, x_s, eps_s, f_s)
zK = z_s * Kval
elapsed = time.time()-t0
print(f"  computed z*K(y,t)f(0) = {mp.nstr(zK, 12)}   (published: 0.9156333394)  [{elapsed:.1f}s]")
report("reproduces published Sec 5.4 value to <1e-8 absolute",
       abs(zK - mp.mpf('0.9156333394')) < mp.mpf('1e-8'),
       f"got {zK}")

# ---------------------------------------------------------------------------
# NEW test: family-uniformity stress grid.
#
# Family: f_k(x') := M*cos(omega*x' + k), M=0.7, omega=0.3, phase k varying
# over {0, pi/4, pi/2, 3pi/4, pi, 5pi/4} -- SAME sup bound M and SAME
# Lipschitz bound M*omega for every member (a rigid family, by
# construction), simulating hypothesis (C')'s requirement that {Phi_t} share
# a uniform-in-t regularity bound while their SHAPE (here: phase) varies --
# exactly the dimension no ancestor (U)-test varied.
# ---------------------------------------------------------------------------
print("\n--- Family-uniformity stress grid (NEW, not tested by any ancestor) ---")
M_amp = mp.mpf('0.7')
omega = mp.mpf('0.3')
phases = [mp.mpf(0), mp.pi/4, mp.pi/2, 3*mp.pi/4, mp.pi, mp.mpf('1.25')*mp.pi]

def make_f(k):
    return lambda u: M_amp * mp.cos(omega*u + k)

x_g = mp.mpf(0)
eps_g = mp.mpf('0.5')
y_g = mp.mpf(100)
z_g = x_g + y_g
h_ratios = [mp.mpf('0.002'), mp.mpf('0.02'), mp.mpf('0.1'), mp.mpf('0.5'), mp.mpf('0.9'), mp.mpf('0.98')]

print(f"  x={x_g}, eps={eps_g}, y={y_g}, z={z_g}")
print(f"  family: f_k(u) = {float(M_amp)}*cos({float(omega)}*u + k), "
      f"k in {[mp.nstr(p,4) for p in phases]}")
print(f"  h/y ratios: {[mp.nstr(r,4) for r in h_ratios]}")
print()
print(f"  {'h/y':>8} {'phase k':>10} {'z^2*remainder':>16}")

results = {}
t0 = time.time()
for ratio in h_ratios:
    h_val = ratio * y_g
    t_val = y_g - h_val
    row = []
    for k in phases:
        f_k = make_f(k)
        Kv = K_full(y_g, t_val, x_g, eps_g, f_k)
        CFv = closed_form(y_g, t_val, x_g, eps_g, f_k)
        remainder = Kv - CFv
        z2rem = z_g**2 * remainder
        row.append(z2rem)
        print(f"  {mp.nstr(float(ratio),4):>8} {mp.nstr(float(k),4):>10} {mp.nstr(z2rem,8):>16}")
    results[ratio] = row
elapsed = time.time()-t0
print(f"\n  [{elapsed:.1f}s total for {len(h_ratios)*len(phases)} kernel evaluations]")

all_vals = [v for row in results.values() for v in row]
max_abs = max(abs(v) for v in all_vals)
min_abs = min(abs(v) for v in all_vals)
print(f"\n  max|z^2*remainder| across full grid = {mp.nstr(max_abs,6)}")
print(f"  min|z^2*remainder| across full grid = {mp.nstr(min_abs,6)}")

# Check: bounded across the WHOLE grid (both dimensions), no blowup, and no
# systematic drift with phase k at fixed ratio (would indicate the constant
# depends badly on the family member, i.e. on a feature (C') would need to
# control).
report("z^2*remainder stays bounded (<10) across the full 2D grid "
       "(h/y ratio x family phase)", max_abs < mp.mpf('10'),
       f"max={max_abs}")

# Quantify phase-sensitivity at fixed ratio: spread (max-min over k) should
# be small relative to the typical magnitude, i.e. the remainder constant is
# not wildly different across family members at the SAME (z,h).
print("\n  Phase-sensitivity at each fixed h/y ratio (max-min over the 6 phases):")
max_spread = mp.mpf(0)
for ratio, row in results.items():
    spread = max(row) - min(row)
    max_spread = max(max_spread, abs(spread))
    print(f"    h/y={mp.nstr(float(ratio),4)}: spread={mp.nstr(spread,6)}  "
          f"(values range {mp.nstr(min(row),4)} to {mp.nstr(max(row),4)})")
report("phase-spread stays modest (<3) at every ratio -- no evidence of a "
       "family member causing the remainder constant to blow up",
       max_spread < mp.mpf('3'), f"max_spread={max_spread}")

print("\n" + "="*78)
print("ALL CHECKS PASSED.")
print("Conclusion: on this 2D grid (h/y ratio x Lipschitz-bounded family")
print("member), the closed form's O(1/z^2) remainder constant is bounded")
print("and does not show a trend toward blowup as the test function's SHAPE")
print("varies within a fixed (sup-norm, Lipschitz) envelope -- genuine new")
print("numerical support for hypothesis (U)+(C') combined, in exactly the")
print("dimension (family variation, not just h/y ratio) no ancestor tested.")
print("This is SUPPORT, not a proof -- see ATTEMPT.md for the precise scope")
print("of what this test does and does not establish.")
print("="*78)
