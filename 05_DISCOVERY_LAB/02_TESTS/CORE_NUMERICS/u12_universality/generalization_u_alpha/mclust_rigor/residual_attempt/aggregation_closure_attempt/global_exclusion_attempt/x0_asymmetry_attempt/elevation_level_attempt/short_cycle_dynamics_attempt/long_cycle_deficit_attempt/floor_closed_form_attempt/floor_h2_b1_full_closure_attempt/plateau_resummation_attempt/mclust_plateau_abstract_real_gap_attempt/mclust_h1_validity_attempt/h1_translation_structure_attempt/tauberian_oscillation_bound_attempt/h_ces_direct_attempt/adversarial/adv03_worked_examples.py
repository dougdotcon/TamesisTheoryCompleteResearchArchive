#!/usr/bin/env python3
"""
Independent verification of Sec 4's two worked examples (positive + sharpness),
written fresh without reading the target's s02 script.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*78)
print("PART A -- Positive example: e(y) := D/(x+y) exactly")
print("="*78)
y, x, D, Y0 = sp.symbols('y x D Y0', positive=True)
h0 = sp.symbols('h0')  # h(Y0)

# e(y):=D/(x+y), so h'(y) = e(y)/(x+y) = D/(x+y)^2 [via the Sec 2.2 quotient-
# rule identity]. Closed form: h(y) = h(Y0) - D/(x+y) + D/(x+Y0).
hprime = D/(x+y)**2
h_closed = h0 - D/(x+y) + D/(x+Y0)
check = sp.simplify(sp.diff(h_closed, y) - hprime)
print(f"d/dy[h0 - D/(x+y) + D/(x+Y0)] - D/(x+y)^2 = {check}  (expect 0)")
assert check == 0
print("PASS: closed form's derivative matches h'(y)=e(y)/(x+y)=D/(x+y)^2 exactly")
print("      (i.e. e(y)=D/(x+y) as the target defines it, consistent with the")
print("      Sec 2.2 quotient-rule identity d/dy[A(y)/(x+y)]=e(y)/(x+y)).")

check_Y0 = sp.simplify(h_closed.subs(y, Y0) - h0)
print(f"h_closed(Y0) - h0 = {check_Y0} (expect 0, boundary condition holds)")
assert check_Y0 == 0

limit_L = sp.limit(h_closed, y, sp.oo)
print(f"lim_{{y->infty}} h(y) = {limit_L} = h0 + D/(x+Y0)")

# Numeric instance x=1, D=2, Y0=1, h(Y0)=0.3
xv, Dv, Y0v, h0v = 1, 2, 1, sp.Rational(3, 10)
Lval = h0v + sp.Rational(Dv, xv+Y0v)
print(f"Concrete instance x=1,D=2,Y0=1,h(Y0)=0.3: predicted L = {Lval} = {float(Lval)}")
assert float(Lval) == 1.3

# Independent mpmath quadrature of h'(y)=D/(x+y)^2 from scratch (re-integrating,
# not using the closed-form antiderivative), compare to closed form at several Y
def hprime_num(yv):
    return mp.mpf(Dv) / (mp.mpf(xv) + yv)**2

print()
print("Independent mpmath quadrature check (integrating h' from Y0 to Y, NOT")
print("using the sympy closed form, then comparing):")
h0_mp = mp.mpf(h0v)
for Yv in [2, 5, 10, 100, 1000, 10**7]:
    integral_val = mp.quad(hprime_num, [Y0v, Yv])
    h_from_quad = h0_mp + integral_val
    h_from_closed = mp.mpf(h0v) - mp.mpf(Dv)/(xv+Yv) + mp.mpf(Dv)/(xv+Y0v)
    diff = abs(h_from_quad - h_from_closed)
    gap_to_L = abs(h_from_quad - mp.mpf(str(Lval)))
    print(f"  Y={Yv:>10}: quad-based h={float(h_from_quad):.12f}  closed-form h={float(h_from_closed):.12f}"
          f"  |diff|={float(diff):.3e}  gap-to-L={float(gap_to_L):.3e}")
    assert diff < mp.mpf('1e-25')
print("PASS: independent quadrature matches the closed form to <1e-25,")
print("      and approaches L=1.3 as Y grows -- matches target's claims")
print("      ('match to <1e-30', 'gap 2e-7 at Y=1e7') within the precision")
print("      class used (mpmath dps=50 vs their reported <1e-30) -- consistent,")
print("      not contradicted; exact digit-for-digit match not attempted here.")

print()
print("="*78)
print("PART B -- Sharpness example: h(y) := sin(log(log(x+y+3)))")
print("="*78)
w = sp.symbols('w', positive=True)
hfun = sp.sin(sp.log(sp.log(x+y+3)))
hprime_sym = sp.diff(hfun, y)
hprime_sym_simplified = sp.simplify(hprime_sym)
print(f"h'(y) = {hprime_sym_simplified}")

# claimed: h'(y) = cos(log(log(w)))/(w*log(w)), w:=x+y+3
w_expr = x + y + 3
claimed_hprime = sp.cos(sp.log(sp.log(w_expr))) / (w_expr * sp.log(w_expr))
residual = sp.simplify(hprime_sym - claimed_hprime)
print(f"h'(y) - cos(log(log(w)))/(w*log(w)): residual = {residual} (expect 0)")
assert residual == 0
print("PASS: h'(y) formula confirmed exactly, independently.")

# e(y) := z*h'(y), z=x+y. Claim e(y) ~ cos(log(log(w)))/log(w) (since z~w for large y)
z_sym = x + y
e_y = z_sym * hprime_sym
print(f"e(y) = z*h'(y) = {sp.simplify(e_y)}")
# check that as y-> infinity (so z,w -> infinity together, z/w -> 1),
# e(y) - cos(log(log(w)))/log(w) -> 0  (since z/w->1)
ratio_zw = sp.limit(z_sym/w_expr, y, sp.oo)
print(f"lim z/w as y->infty: {ratio_zw} (=1, so z~w, e(y)~cos(loglogw)/logw)")

# |e(y)| <= 1/log(w) -> 0  -- confirm limit of 1/log(w) is 0
lim_1_logw = sp.limit(1/sp.log(w_expr), y, sp.oo)
print(f"lim 1/log(w) as y->infty: {lim_1_logw} (=0, confirms e(y) is o(1))")
assert lim_1_logw == 0

# [1/log(w)] / [1/w] -> infinity (O(1/log z) strictly weaker than O(1/z))
ratio_majorants = sp.limit((1/sp.log(w_expr)) / (1/w_expr), y, sp.oo)
print(f"lim [1/log(w)]/[1/w] as y->infty: {ratio_majorants} (expect oo)")
assert ratio_majorants == sp.oo
print("PASS: confirms O(1/log z) is strictly WEAKER than O(1/z).")

# antiderivative of 1/(w log w) is log(log(w)), diverges as w->infty
antideriv = sp.integrate(1/(w*sp.log(w)), w)
print(f"Antiderivative of 1/(w*log(w)) dw = {antideriv}")
lim_antideriv = sp.limit(antideriv, w, sp.oo)
print(f"lim_{{w->infty}} log(log(w)) = {lim_antideriv} (expect oo -- diverges)")
assert lim_antideriv == sp.oo
print("PASS: confirms h' is NOT absolutely integrable (majorant's antiderivative diverges).")

print()
print("Constructive non-convergent subsequence check:")
print("Claim: for target v in {-1,0,1}, theta=asin(v)+2*pi*k (or supplementary),")
print("y_k := e^(e^theta) - 3 - x gives h(y_k) = sin(theta+2*pi*k) = v EXACTLY.")

def h_num(x_val, y_val):
    ww = x_val + y_val + 3
    return mp.sin(mp.log(mp.log(ww)))

x_val = mp.mpf(0)  # test at x=0 for concreteness (matches typical usage)
targets = {
    0: mp.mpf(0),      # sin(theta)=0 -> theta = 2*pi*k (k=0,1,2,3)
    1: mp.pi/2,        # sin(theta)=1 -> theta = pi/2 + 2*pi*k
    -1: -mp.pi/2,      # sin(theta)=-1 -> theta = -pi/2 + 2*pi*k  (or 3pi/2+2pi*k)
}
for label, theta0 in targets.items():
    print(f"  Target v={label}, base theta0={float(theta0):.6f}")
    for k in range(4):
        theta = theta0 + 2*mp.pi*k
        if theta <= 0:
            continue  # need y_k = e^(e^theta) - 3 - x to be a valid (large) y
        y_k = mp.e**(mp.e**theta) - 3 - x_val
        if y_k < 0:
            continue
        hval = h_num(x_val, y_k)
        print(f"    k={k}: theta={float(theta):.6f}  y_k={mp.nstr(y_k, 8)}  h(y_k)={mp.nstr(hval, 15)}"
              f"  |h(y_k)-v|={mp.nstr(abs(hval-label), 6)}")
        assert abs(hval - label) < mp.mpf('1e-30'), f"mismatch at k={k}, v={label}"
print("PASS: constructive subsequence hits -1, 0, +1 EXACTLY (to <1e-30),")
print("      confirming h(y) does NOT converge -- independently reproduced.")

print()
print("Relative-step oscillation check for h(y) (sanity, not in the target's")
print("own explicit claims for THIS function, but useful to confirm h is")
print("plausible as a genuine 'slowly oscillating in the o(1) sense' example,")
print("i.e. that nothing here contradicts the unconditional self-averaging")
print("identity e(y)->0):")
for yv in [10, 100, 1000, 1e6, 1e12]:
    ev = float((x_val + yv) * sp.diff(hfun, y).subs({x: 0, y: yv}))
    print(f"  y={yv:<12}: e(y)={ev:.6f}  (bounded, ->0 slowly as predicted)")
