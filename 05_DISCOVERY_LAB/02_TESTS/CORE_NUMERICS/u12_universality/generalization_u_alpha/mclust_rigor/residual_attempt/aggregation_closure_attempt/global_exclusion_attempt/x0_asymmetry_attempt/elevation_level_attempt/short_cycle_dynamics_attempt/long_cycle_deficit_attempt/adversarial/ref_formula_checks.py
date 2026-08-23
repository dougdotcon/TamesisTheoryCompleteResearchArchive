"""
ref_formula_checks.py -- referee's formula/arithmetic audit of
long_cycle_deficit_attempt/ATTEMPT.md and DERIVATION_PREREG.md.

Not a Monte Carlo script: deterministic checks only, run once, output
captured to ref_formula_checks.log. Uses sc_formula.py (parent front,
already adversarially verified) plus an independent scipy.integrate.quad
cross-check of phi_U, per the mandate's explicit permission to import
sc_formula.py.
"""
import sys
import numpy as np
from scipy import integrate

PARENT_DIR = ("/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/"
              "02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/"
              "mclust_rigor/residual_attempt/aggregation_closure_attempt/"
              "global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/"
              "short_cycle_dynamics_attempt")
sys.path.insert(0, PARENT_DIR)
import sc_formula as F  # noqa: E402


def phiU_quad(c):
    val, _ = integrate.quad(lambda t: np.exp(-c * t * t), 0, 1)
    return val


n = 65536
print("=== (1) phi_U(c) cross-check: scipy.integrate.quad vs sc_formula.phi_U ===")
for c in [1000, 100, 150]:
    q = phiU_quad(c)
    f = F.phi_U(c)
    print(f"  c={c:5d}  quad={q:.8f}  sc_formula={f:.8f}  rel_err={abs(q-f)/q:.2e}")

print("\n=== (2) T1 table's phi_U(c) column -- do the front's numbers match? ===")
refs = {"A": (1000, 0.028025), "B": (100, 0.088623), "C": (150, 0.072360)}
for label, (c, reported) in refs.items():
    computed = F.phi_U(c)
    print(f"  cell {label} c={c:5d}: reported={reported:.6f}  computed={computed:.6f}  "
          f"match={'YES' if abs(reported-computed) < 5e-7 else 'NO'}")

print("\n=== (3) T2 table's rho / phi_U(c'') columns, c=1000, n=65536 ===")
reported_rho = {1: 0.0153, 5: 0.0740, 20: 0.2645, 50: 0.5363, 100: 0.7848}
reported_phiUcpp = {1: 0.028025, 5: 0.028900, 20: 0.032433, 50: 0.040846, 100: 0.059993}
for b in [1, 5, 20, 50, 100]:
    cpp = F.c_double_prime(b, 1000, n)
    rho_formula = F.rho_of(b, 1000, n)
    phiUcpp = F.phi_U(cpp)
    print(f"  b={b:4d}  rho_formula={rho_formula:.5f} (reported {reported_rho[b]:.4f})  "
          f"phi_U(c'')={phiUcpp:.6f} (reported {reported_phiUcpp[b]:.6f})  "
          f"phi_U(c'') match={'YES' if abs(phiUcpp-reported_phiUcpp[b]) < 5e-7 else 'NO'}")

print("\n=== (4) at b=1: c'' = c exactly? (c_double_prime formula check) ===")
for c in [1000, 100, 150]:
    cpp = F.c_double_prime(1, c, n)
    print(f"  c={c:5d}: c''(b=1) = {cpp}  (exactly c: {'YES' if cpp == c else 'NO'})")

print("\n=== (5) pre-registered T1 classification-rule arithmetic ===")
checks = [
    ("11.30/14.7 (cell B ratio, claimed ~77%)", 11.30/14.7, 0.77),
    ("8.60/10.7 (cell C ratio, claimed ~80%)", 8.60/10.7, 0.80),
]
for desc, val, claimed in checks:
    print(f"  {desc}: computed={val*100:.2f}%  claimed~{claimed*100:.0f}%  "
          f"{'OK' if abs(val-claimed) < 0.01 else 'MISMATCH'}")

print("\n=== (6) pre-registered T2 classification-rule arithmetic ===")
checks2 = [
    ("8.95/2.89 (max/min ratio, claimed 3.10x)", 8.95/2.89, 3.10),
    ("8.95/3.42 (b100/b1 ratio, claimed 2.62x)", 8.95/3.42, 2.62),
    ("3.42/8.95 (b1 fraction of full deficit, claimed 38.2%)", 3.42/8.95, 0.382),
]
for desc, val, claimed in checks2:
    unit = 100 if val < 1.5 else 1
    print(f"  {desc}: computed={val:.4f}  claimed={claimed}  "
          f"{'OK' if abs(val-claimed) < 0.02*max(1,claimed) else 'MISMATCH'}")

print("\n=== (7) post-hoc inverse-variance-weighted combination "
      "(T1 cell A + T2 b=1 point, front's own numbers) ===")
x1, se1 = 0.027319, 0.000296   # T1 cell A (front)
x2, se2 = 0.027067, 0.000332   # T2 b=1 point (front)
phiU = 0.028025
w1, w2 = 1/se1**2, 1/se2**2
wmean = (w1*x1 + w2*x2) / (w1 + w2)
wse = (1/(w1+w2))**0.5
z_diff = (x1-x2) / np.sqrt(se1**2+se2**2)
dev = 100*(wmean-phiU)/phiU
z = (wmean-phiU)/wse
print(f"  z_diff = {z_diff:+.3f}  (claimed +0.57)")
print(f"  combined dev% = {dev:+.3f}  (claimed -2.92%)")
print(f"  combined z    = {z:+.3f}  (claimed -3.70)")

print("\n=== (8) reference-figure provenance check: '-9.66%' for cell A ===")
print("  DERIVATION_PREREG.md sec3 attributes 'cell A -9.66%' to")
print("  short_cycle_dynamics_attempt/ATTEMPT.md sec3.1's own reported figure.")
print("  ATTEMPT.md sec3.1's actual (20b,inf) row for cell '100,1000' (=cell A) is")
print("  '-9.7% (z=-9.4)', n=34.1M -- NOT literally '-9.66%'.")
print("  The literal string '9.66' appears exactly once elsewhere tied to a %")
print("  figure in the whole archive: short_cycle_dynamics_attempt/adversarial/")
print("  REFEREE_REPORT.md line 256 / adv_reduction.log line 43, for cell")
print("  'b=400,c=100' (= this front's OWN cell B, not cell A!), comparing")
print("  measured full-phi against phi_REDC_full (Claim 4's refuted reduction")
print("  formula) -- a DIFFERENT quantity from a DIFFERENT test (sec3.2, not the")
print("  sec4.1 (20b,inf) far-tail-vs-phi_U(c'') table T1 actually reuses).")
print("  CONCLUSION: '-9.66%' is a genuine mis-citation (wrong cell AND wrong")
print("  quantity), coincidentally close in VALUE to the correct cell-A figure")
print("  (-9.7%), so it does not flip cell A's classification, but the framing")
print("  '2.52/9.66=26%, well under 1/3' is reference-choice-fragile: using the")
print("  low end of the front's OWN pre-registered confirmed range for cell A")
print("  (-6.4%, DERIVATION_PREREG.md sec0 / referee's own remeasurement) gives")
print(f"  2.52/6.4 = {100*2.52/6.4:.1f}%, which is NOT 'well under 1/3'.")
