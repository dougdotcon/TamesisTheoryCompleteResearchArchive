"""
a04_ncross_formula_and_translation_invariance.py

(A) Re-derive n! >= (n/e)^n from scratch and verify numerically.
(B) Re-derive n_cross_rigorous(y) = ceil(M*e*y)+1 from scratch and
    reproduce the target's own Sec 4.3 table exactly, independently.
(C) Directly test whether K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t) is a
    function of (y-t) alone (translation-invariant) or genuinely depends
    on y and t separately -- by evaluating the operator's action on a
    concrete test function f(x)=1 at two DIFFERENT (y,t) pairs sharing the
    SAME y-t, and checking whether the results agree.
"""
import mpmath as mp
import math

mp.mp.dps = 40
SQRT_PI_2 = mp.sqrt(mp.pi/2)

print("="*70)
print("PART A: n! >= (n/e)^n, re-derived and checked")
print("="*70)
print("Proof: e^n = sum_{k=0}^inf n^k/k! >= n^n/n! (single term k=n, all")
print("terms of the sum being positive). Rearranging: n! >= n^n/e^n = (n/e)^n.")
for n in [1,2,5,10,20,50,100,500]:
    lhs = mp.factorial(n)
    rhs = mp.mpf(n/mp.e)**n
    print(f"  n={n:>4}: n! = {mp.nstr(lhs,8)}   (n/e)^n = {mp.nstr(rhs,8)}   n!>=(n/e)^n: {lhs>=rhs}")
print()

print("="*70)
print("PART B: n_cross_rigorous(y) := ceil(M*e*y)+1, re-derived from scratch")
print("="*70)
print("Claim: (My)^n/n! <= (My*e/n)^n  [via n!>=(n/e)^n]  < 1  iff  My*e/n < 1")
print("  iff  n > M*y*e.  So n_cross_rigorous(y) := ceil(M*y*e)+1 guarantees")
print("  n >= n_cross_rigorous(y)  =>  n > M*y*e  =>  (My)^n/n! < 1.  Re-derived.")
print()

def n_cross_rigorous(y, M):
    return math.ceil(M*y*math.e) + 1

def M_of(eps):
    return float(SQRT_PI_2) + eps

leading_slope = math.e * float(SQRT_PI_2)
print(f"Leading-order (eps->0) slope: e*sqrt(pi/2) = {leading_slope:.5f}  (target claims 3.40686...)")
print()

print("Reproduction of target's Sec 4.3 table (rigorous bound column):")
table_c100 = [0.5,1.0,2.0,3.0,4.0,5.0,6.0]
table_c1000 = [0.5,1.0,2.0,3.0,4.0,5.0,6.0]
target_reported_c100 = [3,5,9,13,16,20,24]
target_reported_c1000 = [3,5,8,12,15,19,22]

M100 = M_of(1/math.sqrt(100))
M1000 = M_of(1/math.sqrt(1000))
print(f"c=100:  M={M100:.4f}")
ok = True
for y0, tgt in zip(table_c100, target_reported_c100):
    mine = n_cross_rigorous(y0, M100)
    match = (mine == tgt)
    ok = ok and match
    print(f"   y={y0}: mine={mine}  target={tgt}  match={match}")
print(f"c=1000: M={M1000:.4f}")
for y0, tgt in zip(table_c1000, target_reported_c1000):
    mine = n_cross_rigorous(y0, M1000)
    match = (mine == tgt)
    ok = ok and match
    print(f"   y={y0}: mine={mine}  target={tgt}  match={match}")
print(f"\nAll match: {ok}")
print()
print("Also verify strict inequality/monotone-decrease claim: term(n+1)/term(n)")
print("= My/(n+1); once n+1 > My, ratio < 1 and is itself decreasing in n")
print("(since My/(n+1) shrinks as n grows) -- so once (My)^n/n!<1 is first")
print("achieved, the SEQUENCE (My)^n/n! is thereafter strictly decreasing,")
print("confirmed symbolically (ratio formula is a decreasing function of n")
print("for n+1>My>0, trivial calculus) and numerically below:")
for y0, M in [(3.0, M100), (6.0, M1000)]:
    My = M*y0
    n0 = n_cross_rigorous(y0, M)
    terms = [(My**n)/math.factorial(n) for n in range(n0, n0+6)]
    print(f"  y={y0}, M={M:.3f}: terms n={n0}..{n0+5}: {[f'{t:.3e}' for t in terms]}")
    decreasing = all(terms[i] > terms[i+1] for i in range(len(terms)-1))
    print(f"    strictly decreasing: {decreasing}")

print()
print("="*70)
print("PART C: is K(y,t) translation-invariant in (y,t), i.e. a function of")
print("(y-t) alone?  Direct test on a concrete test function f(x)=1.")
print("="*70)
print("K(y,t) = M_y o K_A^raw(y,t) + K_B(y-t)")
print("  K_B(h) = int_0^h e^{-v/eps} S_v dv          -- manifestly depends on h=y-t ONLY")
print("  M_y o K_A^raw(y,t) acting on f=1, at x=0:")
print("    (K_A^raw(y,t)[1])(0) = int_t^y e^{-(y-w)/eps} * (T_w[1])(0-(y-w)) ... ")
print("  -- easier: use the CLOSED bound-derivation's own reduction (Sec 2 of the")
print("  target, re-derived independently in a01): the exact identity gives")
print("    (K_A^raw(y,t)[1])(x) <= eps*R(x+y)  with equality structure")
print("  and more precisely, from Sec 4.1 of h1_volterra_attempt (cited, re-derived")
print("  in a01/a05): (S_{y-w}T_w[1])(x) = int_0^inf e^{-u^2/2-u(x+y)} du = R(x+y)")
print("  (independent of w!), so")
print("    (K_A^raw(y,t)[1])(x) = R(x+y) * int_t^y e^{-(y-w)/eps} dw")
print("                          = R(x+y) * eps*(1-e^{-(y-t)/eps})")
print("  and  (M_y K_A^raw(y,t)[1])(x) = [(1-eps(x+y))/eps] * R(x+y) * eps*(1-e^{-(y-t)/eps})")
print("                                = (1-eps(x+y))*R(x+y) * (1-e^{-(y-t)/eps})")
print()
print("This factors as [function of (x,y) ONLY] * [function of (y-t) ONLY].")
print("Since the SECOND factor depends only on h:=y-t, but the FIRST factor,")
print("(1-eps(x+y))*R(x+y), depends on y directly (not merely on y-t), the")
print("full expression is translation-invariant in (y,t) ONLY IF x is allowed")
print("to co-vary with y -- but x is an INDEPENDENT coordinate (the Banach-")
print("space index), so at FIXED x, K(y,t)[1](x) genuinely depends on y and")
print("t separately (through y alone, in the first factor), not merely on h=y-t.")
print()
print("Direct numerical check: fix x=0, h=y-t=1.0, vary y (=t+1) and confirm")
print("(M_y K_A^raw(y,t)[1])(0) is NOT constant as y varies at fixed h:")

def R_mp(z):
    z = mp.mpf(z)
    return mp.sqrt(mp.pi/2)*mp.erfc(z/mp.sqrt(2))*mp.e**(z*z/2)

def MyKAraw_on_1(x, y, t, eps):
    x=mp.mpf(x); y=mp.mpf(y); t=mp.mpf(t); eps=mp.mpf(eps)
    h = y-t
    return (1-eps*(x+y))*R_mp(x+y)*(1-mp.e**(-h/eps))

eps = mp.mpf('0.1')
x0 = mp.mpf(0)
h = mp.mpf('1.0')
print(f"  (eps={float(eps)}, x=0, h=y-t=1.0 fixed)")
for y0 in [1.0, 2.0, 5.0, 10.0, 50.0]:
    t0 = y0 - float(h)
    val = MyKAraw_on_1(x0, y0, t0, eps)
    print(f"    y={y0:>6}, t={t0:>6}, y-t={float(h)}: (M_y K_A^raw(y,t)[1])(0) = {float(val):.8f}")
print()
print("CONCLUSION: the value visibly changes as y grows at FIXED h=y-t -- K(y,t)")
print("is NOT translation-invariant in (y,t); confirms the target's Claim 4")
print("by direct, independent computation (not merely restating the target's")
print("own structural argument).")
print()
print("Also check: is there an OBVIOUS reformulation that restores translation")
print("invariance (e.g. a substitution absorbing the y-dependence)? The first")
print("factor (1-eps(x+y))*R(x+y) depends on the SUM x+y, i.e. it IS translation-")
print("invariant along characteristics x+y=const (matching the x+y-conservation")
print("structural fact already established in the required reading) -- but x")
print("and y are independently-varying coordinates of the Banach-space-valued")
print("problem (x indexes the FUNCTION SPACE, y is the Volterra 'time'), so")
print("fixing x and varying y necessarily moves x+y too. No reparametrization")
print("that holds x fixed (as the Banach-space evaluation point) can remove")
print("this: translation invariance in (y,t) would require the kernel to")
print("depend on (y-t) ALONE for every fixed x, which the x+y-dependence of")
print("the first factor directly rules out. The target's identification of")
print("this obstacle appears CORRECT and not resolvable by a missed change of")
print("variables at fixed x.")
