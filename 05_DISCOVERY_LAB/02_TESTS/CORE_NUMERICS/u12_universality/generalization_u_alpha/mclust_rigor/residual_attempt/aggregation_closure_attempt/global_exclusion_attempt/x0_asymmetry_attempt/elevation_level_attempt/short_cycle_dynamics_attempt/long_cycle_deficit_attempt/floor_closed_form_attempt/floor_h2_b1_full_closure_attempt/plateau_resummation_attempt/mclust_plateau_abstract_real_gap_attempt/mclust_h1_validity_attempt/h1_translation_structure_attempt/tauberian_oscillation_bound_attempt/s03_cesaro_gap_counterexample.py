"""
s03_cesaro_gap_counterexample.py

TAUBERIAN-OSCILLATION-BOUND-ATTEMPT, wave 26 front (c).

The classical continuous Tauberian theorem for Cesaro-(C,1) summability
(quoted, cited, in h1_translation_structure_attempt Sec 6.3) has THREE
hypotheses on a bounded g:[0,inf)->R, not two:
  (H-bdd)   g bounded
  (H-ces)   (1/y) int_0^y g(t) dt -> L   for SOME L      [Cesaro convergence]
  (H-osc)   g slowly oscillating in the RELATIVE-step sense
and concludes g(y) -> L.

DISC-DEC-122's mandate (and DISC-DEC-123's restatement of it) names only
TWO missing ingredients for closing (U1): (i) an oscillation bound on Phi
of the relative-step form [[H-osc]], and (ii) verification the theorem's
hypotheses transfer to the 2-var PDE setting. This script demonstrates,
via an elementary, fully worked, numerically-confirmed example, that
(H-osc) alone -- even granted unconditionally, as this front's s01/s02
derive for Phi -- does NOT substitute for (H-ces): a bounded function can
be slowly-oscillating in the exact relative-step sense the theorem needs,
have a self-averaging identity trivially satisfied (any g equals its own
Cesaro mean plus an o(1) term is NOT automatic in general, but here we
show something sharper -- see Part 2), and still fail to converge, because
its OWN Cesaro mean ALSO fails to converge. This makes precise and
concrete why establishing (H-ces) -- Cesaro convergence of
A(y)/(x+y) itself -- is a THIRD, logically independent requirement of the
classical theorem, not automatically supplied by an oscillation bound,
and NOT established anywhere in this lineage's record for A(y)/(x+y).

Written FRESH; elementary calculus, sympy for the exact antiderivative,
mpmath for numerical confirmation of non-convergence.
"""
import sympy as sp
import mpmath as mp

print("=" * 92)
print("PART 1: g(t) := sin(log(1+t)) is bounded and slowly-oscillating")
print("(relative-step sense) -- verified symbolically/analytically")
print("=" * 92)

t, y, s, delta = sp.symbols('t y s delta', positive=True, real=True)
g = sp.sin(sp.log(1 + t))
print(f"g(t) = {g}")
print(f"|g(t)| <= 1 for all t>=0: trivial (sin is bounded).  (H-bdd) HOLDS.")
print()

# Relative-step oscillation: g(s)-g(y) for s-y <= delta*y, s=y*(1+delta_frac)
delta_frac = sp.symbols('delta_frac', positive=True)
s_expr = y * (1 + delta_frac)
diff_expr = sp.sin(sp.log(1 + s_expr)) - sp.sin(sp.log(1 + y))
# Taylor in delta_frac around 0, for fixed y -> infinity
series_check = sp.series(diff_expr, delta_frac, 0, 2).removeO()
print("g(y(1+delta_frac)) - g(y), series in delta_frac (fixed y), to O(delta_frac^2):")
sp.pprint(series_check)
# as y -> infinity, the y-dependence of the leading term:
leading_coeff = sp.limit(sp.diff(diff_expr, delta_frac).subs(delta_frac, 0), y, sp.oo)
print(f"\nleading coefficient (d/d(delta_frac) at 0) as y->infinity: does NOT")
print(f"simplify to a constant (it is cos(log(1+y)) * y/(1+y), itself bounded")
print(f"by 1 in absolute value for ALL y) -- so |g(s)-g(y)| <= delta_frac + o(delta_frac)")
print(f"UNIFORMLY in y, for ALL y>=0 (no exceptional points, unlike a")
print(f"piecewise-constant construction with boundaries). This IS the exact")
print(f"(H-osc) relative-step condition, genuinely satisfied for ALL y, not")
print(f"just asymptotically or on a subsequence.")
print()
print("Numerical confirmation at several y, delta_frac=0.01,0.05,0.1:")
gf = sp.lambdify(t, g, 'mpmath')
mp.mp.dps = 25
for yv in (10, 100, 1000, 10000):
    row = []
    for dv in (0.01, 0.05, 0.1):
        sv = yv * (1 + dv)
        diff = abs(gf(sv) - gf(yv))
        row.append(f"delta={dv}: |g(s)-g(y)|={float(diff):.5f} (<=delta? "
                    f"{'YES' if diff <= dv + 1e-9 else 'no, but O(delta)'})")
    print(f"  y={yv:6d}: " + " | ".join(row))

print()
print("=" * 92)
print("PART 2: g's own Cesaro mean, (1/y) int_0^y g(t) dt, computed EXACTLY")
print("=" * 92)

# exact antiderivative via substitution t = e^u - 1
u = sp.symbols('u', real=True)
antideriv_u = sp.integrate(sp.sin(u) * sp.exp(u), u)
antideriv_u = sp.simplify(antideriv_u)
print(f"Substituting t=e^u-1 (dt=e^u du): int sin(u)*e^u du = {antideriv_u}")

Y = sp.symbols('Y', positive=True, real=True)
u_hi = sp.log(1 + Y)
F = antideriv_u
exact_integral = sp.simplify(F.subs(u, u_hi) - F.subs(u, 0))
print(f"\nint_0^Y g(t) dt = {sp.simplify(exact_integral)}")
cesaro_mean = sp.simplify(exact_integral / Y)
print(f"\nCesaro mean (1/Y) int_0^Y g(t) dt = {sp.simplify(cesaro_mean)}")

# Verify by direct differentiation that d/dY[exact_integral] = g(Y)
# SELF-CAUGHT BUG (harness, caught on first run): the line below originally
# compared against the bare symbol `g` (built from free variable `t`), not
# `g` evaluated AT `Y` -- producing a spurious residual that still contains
# the unrelated free symbol `t`, immediately flagging it as a harness bug,
# not a mathematical failure (a genuine residual cannot contain a variable
# unrelated to the equation being checked). Fixed by substituting t->Y.
g_at_Y = g.subs(t, Y)
check = sp.simplify(sp.diff(exact_integral, Y) - g_at_Y)
print(f"\n[check] d/dY[int_0^Y g dt] - g(Y) = {check}  (should be 0)")
assert check == 0, "FAIL: antiderivative check failed"
print("-> PASS: exact antiderivative confirmed by direct differentiation.")

print()
print("=" * 92)
print("PART 3: NEITHER g(Y) NOR its Cesaro mean converges as Y->infinity")
print("(both oscillate with the SAME non-vanishing amplitude)")
print("=" * 92)
cesaro_limit_form = sp.simplify(sp.limit(cesaro_mean - (sp.sin(sp.log(1+Y)) -
                                 sp.cos(sp.log(1+Y)))/2, Y, sp.oo))
print(f"Cesaro mean - (1/2)(sin(log(1+Y))-cos(log(1+Y)))  ->  {cesaro_limit_form}  as Y->inf")
print("(i.e. the Cesaro mean is asymptotically (1/2)(sin(log(1+Y))-cos(log(1+Y))),")
print(" an oscillation of amplitude sqrt(2)/2, NOT a convergent sequence.)")
print()
cesf = sp.lambdify(Y, cesaro_mean, 'mpmath')
print(f"{'Y':>10} {'g(Y)':>12} {'Cesaro mean':>14}")
for Yv in (10, 100, 1000, 1e4, 1e5, 1e6, 1e7, 1e8):
    gv = gf(mp.mpf(Yv))
    cv = cesf(mp.mpf(Yv))
    print(f"{Yv:10.0e} {float(gv):12.6f} {float(cv):14.6f}")
print()
print("Both columns keep oscillating without settling, no matter how large Y")
print("gets -- CONFIRMING that (H-bdd)+(H-osc) alone, without an independently")
print("established (H-ces), do NOT imply convergence. The relative-step")
print("oscillation bound this front derives for Phi (s01/s02) is therefore")
print("NOT, by itself, sufficient input to the classical Tauberian theorem --")
print("Cesaro convergence of A(y)/(x+y) must ALSO be established, separately,")
print("and is NOT addressed by (i) or by the self-averaging identity (which")
print("only says Phi_y(x) and A(y)/(x+y) differ by o(1) -- it does not, and")
print("cannot, say anything about whether A(y)/(x+y) itself has a limit).")
