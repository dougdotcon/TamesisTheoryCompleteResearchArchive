"""
Adversarial independent numerical re-verification, ATTEMPT.md Section 5.

(A) Independently re-derive and check the analytic bound R(x) <= 1/x for x>0.
(B) Independently spot-check psi1..psi4 at the physical edge x=sqrt(c) for a
    SUBSET of the front's own c-grid (c=1000, 4000, 8000 chosen here -- 3 of
    the 6), using an INDEPENDENT numerical implementation:
      - R(x) via mpmath's BUILT-IN erfc (mpmath.erfc(x/sqrt2)*sqrt(pi/2)*exp(x^2/2)),
        which is a DIFFERENT numerical route than the front's own fix (a
        substituted quad integral) -- if both give the same answer, that is
        a genuine independent cross-check, not a re-run of the same method.
      - R', R'', R''' via the elementary derivative-closure recursion
        R^{(n+1)} = x R^{(n)} + n R^{(n-1)}, re-derived directly here by hand
        from R' = xR - 1 (differentiate repeatedly).
      - psi3(x) via the Growth-Exclusion Lemma's own bounded-branch formula
        (Section 2) applied to source f(x) = 7*R'(x):
          psi3(x) = -e^{x^2/2} int_x^inf e^{-t^2/2} * 7 R'(t) dt
        computed via the numerically-safe substitution t = x+u (own
        derivation, avoiding the huge-prefactor-times-tiny-tail pitfall the
        front's own S1 names), i.e.
          psi3(x) = -int_0^inf e^{-xu-u^2/2} * 7 R'(x+u) du
      - psi4(x) = (17/3) R'''(x), the record's own closed form, via our own
        R''' from the derivative recursion (not copied from any script).

No .py file from the target front or any ancestor front was opened.
"""
import mpmath as mp

mp.mp.dps = 60

print("="*70)
print("PART A: independent proof and numerical check of R(x) <= 1/x, x>0")
print("="*70)
print("""
Re-derivation (from scratch): For t >= x > 0,  t/x >= 1, so
    e^{-t^2/2} <= (t/x) e^{-t^2/2}.
Integrating both sides over t in [x, infinity):
    int_x^inf e^{-t^2/2} dt <= (1/x) int_x^inf t e^{-t^2/2} dt = (1/x) e^{-x^2/2}
(since d/dt[-e^{-t^2/2}] = t e^{-t^2/2}, so int_x^inf t e^{-t^2/2}dt = e^{-x^2/2} exactly).
Multiply both sides by e^{x^2/2}:
    R(x) = e^{x^2/2} int_x^inf e^{-t^2/2} dt <= 1/x.   QED (elementary, x>0).
""")

def R_builtin(x):
    x = mp.mpf(x)
    return mp.sqrt(mp.pi/2) * mp.e**(x**2/2) * mp.erfc(x/mp.sqrt(2))

xs_test = [0.5, 1, 2, 5, 10, 20, 31.622776601683793, 50, 89.44271909999159, 150, 200]
print(f"{'x':>10} | {'R(x)':>26} | {'1/x':>26} | R(x)<=1/x?")
all_bound_ok = True
for xv in xs_test:
    Rv = R_builtin(xv)
    bound = mp.mpf(1)/mp.mpf(xv)
    ok = Rv <= bound
    all_bound_ok &= ok
    print(f"{xv:>10} | {mp.nstr(Rv,18):>26} | {mp.nstr(bound,18):>26} | {ok}")
assert all_bound_ok
print("\nPASS: R(x) <= 1/x confirmed numerically (independent erfc-based route) at all test x,")
print("      including x=sqrt(1000)=31.62 and x=sqrt(8000)=89.44, the physical-edge values")
print("      relevant to Part B below.\n")

print("="*70)
print("PART B: independent physical-edge (x=sqrt(c)) spot check, psi1..psi4")
print("="*70)

def R(x):
    return R_builtin(x)

def Rprime(x):
    x = mp.mpf(x)
    return x*R(x) - 1

def Rpp(x):
    x = mp.mpf(x)
    return R(x) + x*Rprime(x)

def Rppp(x):
    x = mp.mpf(x)
    return 2*Rprime(x) + x*Rpp(x)

def psi1(x):
    return R(x)

def psi2(x):
    x = mp.mpf(x)
    return 2*x*R(x) - 2

def psi3(x):
    """Growth-Exclusion Lemma bounded-branch formula, source f(t)=7*R'(t):
       psi3(x) = -e^{x^2/2} int_x^inf e^{-t^2/2} 7 R'(t) dt
       computed via the substitution t = x+u (own derivation):
       psi3(x) = -int_0^inf e^{-x*u - u^2/2} 7 R'(x+u) du
    """
    x = mp.mpf(x)
    integrand = lambda u: mp.e**(-x*u - u**2/2) * 7 * Rprime(x+u)
    # split the quad into a few segments for robustness at large x (kernel
    # e^{-x*u} decays fast; concentrate nodes near u=0)
    val = mp.quad(integrand, [0, 1/max(x,mp.mpf(1)), 5/max(x,mp.mpf(1)), 20, mp.inf])
    return -val

def psi4(x):
    x = mp.mpf(x)
    return mp.mpf(17)/3 * Rppp(x)

# Sanity checks at x=0 against the record's own closed forms (before trusting
# these implementations at the physical-edge x=sqrt(c) values)
print("Sanity check at x=0 against record's own closed forms:")
psi1_0 = psi1(0)
psi2_0 = psi2(0)
psi3_0 = psi3(0)
psi4_0 = psi4(0)
print("psi1(0) =", mp.nstr(psi1_0, 25), " expect sqrt(pi/2) =", mp.nstr(mp.sqrt(mp.pi/2), 25))
print("psi2(0) =", mp.nstr(psi2_0, 25), " expect -2")
print("psi3(0) =", mp.nstr(psi3_0, 25), " expect (7/2)sqrt(pi/2) =", mp.nstr(mp.mpf(7)/2*mp.sqrt(mp.pi/2), 25))
print("psi4(0) =", mp.nstr(psi4_0, 25), " expect -34/3 =", mp.nstr(-mp.mpf(34)/3, 25))

assert abs(psi1_0 - mp.sqrt(mp.pi/2)) < mp.mpf('1e-40')
assert abs(psi2_0 - (-2)) < mp.mpf('1e-40')
assert abs(psi3_0 - mp.mpf(7)/2*mp.sqrt(mp.pi/2)) < mp.mpf('1e-30')
assert abs(psi4_0 - (-mp.mpf(34)/3)) < mp.mpf('1e-40')
print("PASS: all four x=0 sanity checks match the record's closed forms to >=30 digits.\n")

print("Physical-edge spot check at x=sqrt(c), c in {1000, 4000, 8000}")
print("(chosen as 3 of the front's own 6-value c-grid {200,500,1000,2000,4000,8000})\n")

targets = {
    1000: {"x": mp.sqrt(1000), "psi1": "0.031591248", "psi2": "-0.0019940298",
           "psi3": "0.00022004115", "psi4": "-0.0000336635"},
    4000: {"x": mp.sqrt(4000), "psi1": "0.015807438", "psi2": "-0.0004996255",
           "psi3": "0.000027628502", "psi4": "-0.0000021197"},
    8000: {"x": mp.sqrt(8000), "psi1": "0.011178943", "psi2": "-0.0002499063",
           "psi3": "0.0000097754672", "psi4": "-0.00000053059"},
}

header = f"{'c':>6} | {'x=sqrt(c)':>12} | {'quantity':>6} | {'ours':>20} | {'front (ATTEMPT.md)':>20} | rel diff"
print(header)
all_match = True
for c, info in targets.items():
    x = info["x"]
    my_vals = {"psi1": psi1(x), "psi2": psi2(x), "psi3": psi3(x), "psi4": psi4(x)}
    for key in ["psi1", "psi2", "psi3", "psi4"]:
        mine = my_vals[key]
        theirs = mp.mpf(info[key])
        reldiff = abs(mine - theirs) / abs(theirs)
        ok = reldiff < mp.mpf('1e-5')  # front reported ~8-9 sig figs; be generous but decisive
        all_match &= ok
        print(f"{c:>6} | {mp.nstr(x,10):>12} | {key:>6} | {mp.nstr(mine,15):>20} | {mp.nstr(theirs,15):>20} | {mp.nstr(reldiff,4)}  {'OK' if ok else 'MISMATCH'}")

assert all_match
print("\nPASS: all 12 spot-checked values (3 c-values x 4 profiles) match ATTEMPT.md's")
print("      Section 5.2 table to within the precision the front itself printed,")
print("      via an INDEPENDENT implementation (own erfc-based R, own substituted-quad")
print("      psi3, own derivative-recursion R''').\n")

print("="*70)
print("Monotone-decrease-in-magnitude check across the 3 tested c values")
print("(front's own claim: all four columns strictly decreasing in magnitude as c grows)")
print("="*70)
cs_sorted = sorted(targets.keys())
for key in ["psi1", "psi2", "psi3", "psi4"]:
    vals = [abs(mp.mpf(targets[c][key])) for c in cs_sorted]
    decreasing = all(vals[i] > vals[i+1] for i in range(len(vals)-1))
    print(f"{key}: values at c={cs_sorted} -> magnitudes {[mp.nstr(v,6) for v in vals]}  decreasing={decreasing}")
    assert decreasing
print("\nPASS: monotone decrease in magnitude confirmed on this 3-point subset (consistent")
print("      with, not a full replacement for, the front's own full 6-point check).")

print("\nALL PART A-B NUMERICAL CHECKS PASSED.")
