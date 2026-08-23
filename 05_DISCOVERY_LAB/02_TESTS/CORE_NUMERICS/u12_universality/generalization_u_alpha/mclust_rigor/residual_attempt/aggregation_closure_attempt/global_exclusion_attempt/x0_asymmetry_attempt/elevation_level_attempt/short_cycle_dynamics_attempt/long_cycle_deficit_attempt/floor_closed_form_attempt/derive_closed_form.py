"""Symbolic (sympy, exact) verification of the single-re-entry ("s_E=0")
closed-form candidate (3.1) in DERIVATION_PREREG.md, and a numeric check
that it is a poor/qualitatively-wrong approximation for large t0 (predicts
continued decay, contradicting the plateau established by fcd_t1/t2/t3).

Derivation recap: under the s_E=0 approximation (s=t0-g exactly), the
Volterra equation
  Phi(g) = e^{-cg} + (c/t0) * int_0^g e^{-c*delta} * M(g-delta) d delta,
  M(x) = int_0^x Phi(y) dy
is solved via Laplace transform in g, giving the 2nd-order linear ODE
system M'=e^{-cg}+(c/t0)P, P'=M-cP (P:=e^{-cg}N, N=int_0^g e^{cu}M(u)du),
with closed form
  Phi(g) = [s1 e^{s1 g} - s2 e^{s2 g}] / (s1 - s2),
  s1,2 = (-c +- sqrt(c^2 + 4c/t0)) / 2.
This script (a) re-derives the ODE system's characteristic roots directly
from the Laplace-transform algebra symbolically (sympy), confirming no
transcription error, and (b) evaluates Phi(t0) numerically across the
target cell's range to document the qualitative failure (decay, not
plateau) referenced in ATTEMPT.md.
"""
import sympy as sp

s, c, t0, g = sp.symbols('s c t0 g', positive=True)

# Laplace-domain relations: sM = 1/(s+c) + (c/t0) P ; s P = M - c P  =>  P=M/(s+c)
M_hat = sp.symbols('Mhat')
P_expr = M_hat / (s + c)
eq = sp.Eq(s * M_hat, 1/(s + c) + (c/t0) * P_expr)
M_hat_sol = sp.solve(eq, M_hat)[0]
M_hat_sol = sp.simplify(M_hat_sol)
print("M_hat(s) =", M_hat_sol)

Phi_hat = sp.simplify(s * M_hat_sol)  # Phi_hat = s*M_hat - M(0)=0
print("Phi_hat(s) =", Phi_hat)

# denominator roots
denom = sp.denom(sp.together(Phi_hat))
roots = sp.solve(sp.Eq(denom, 0), s)
print("roots of denominator (should match s1,s2):", roots)

s1_expected = (-c + sp.sqrt(c**2 + 4*c/t0)) / 2
s2_expected = (-c - sp.sqrt(c**2 + 4*c/t0)) / 2
print("expected s1 =", s1_expected, " s2 =", s2_expected)
diffs = [sp.simplify(r - s1_expected) for r in roots] + [sp.simplify(r - s2_expected) for r in roots]
print("root match check (one of these should be exactly 0 for each expected root):")
for d in diffs:
    print("  ", d)

# Inverse Laplace transform check via sympy directly (small case, symbolic c,t0 kept)
t = sp.symbols('t', positive=True)  # dummy Laplace variable name clash avoided
Phi_g = sp.inverse_laplace_transform(Phi_hat, s, g)
Phi_g = sp.simplify(Phi_g)
print("\nInverse Laplace transform (sympy, symbolic):")
sp.pprint(Phi_g)

print("\n--- Numeric evaluation at c=1000, several t0 (documents the decay,")
print("    contradicting the plateau established empirically in fcd_t1/t2/t3) ---")
import numpy as np


def phi_heuristic(t0v, cv):
    beta = cv / t0v
    disc = cv**2 + 4*beta
    sq = np.sqrt(disc)
    s1v = (-cv + sq)/2
    s2v = (-cv - sq)/2
    gv = t0v
    return (s1v*np.exp(s1v*gv) - s2v*np.exp(s2v*gv)) / (s1v - s2v)


for t0v in [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 0.9]:
    print(f"  t0={t0v:.3f}  Phi_heuristic(t0) = {phi_heuristic(t0v, 1000):.6f}")
