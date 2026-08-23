"""
R1: verify Corolario A1's exact closed form for psi_n^{(K)} against the
independently-PROVED closed forms for K=1..5 already established elsewhere
in the archive by completely different methods (wave 5/6 hand derivation,
K=1,2; k3_attempt_2 exact Markov chain, K=3,4,5), cited only as TARGET
values -- everything below is computed fresh, symbolically, in sympy, with
no code reused from any sibling directory.

Corolario A1 (all_orders_closed_form_attempt/ATTEMPT.md, THEOREM.md Estagio 9):

    psi_n^{(K)} = (phi_K / 4^K) * sum_{j=0}^{K} C(2K+1, K-j) * (n+j)! / (n! * n^j)

    phi_r = 4^r (r!)^2 / (2r+1)!

Targets (transcribed only as targets to reproduce, per governance convention
used throughout this lineage):

    psi_n^{(1)} = (4n+1)/(6n)
    psi_n^{(2)} = (8n^2+4n+1)/(15n^2)
    psi_n^{(3)} = (64n^3+48n^2+25n+6)/(140n^3)
    psi_n^{(4)} = (128n^4+128n^3+103n^2+52n+12)/(315n^4)
    psi_n^{(5)} = (...+1405n^3+...)/(2772n^5)   [only the 1/n^2 coefficient,
                  1405/2772, is used elsewhere as a cross-check target; here
                  we reproduce the FULL rational function and read off that
                  same coefficient as an extra check]
"""
import sympy as sp

n = sp.symbols('n', positive=True)


def phi(r):
    r = sp.Integer(r)
    return sp.Rational(4)**r * sp.factorial(r)**2 / sp.factorial(2 * r + 1)


def psi_closed_form(K):
    """Corolario A1, symbolic in n, exact rational function."""
    K = sp.Integer(K)
    total = 0
    for j in range(K + 1):
        term = sp.binomial(2 * K + 1, K - j) * sp.factorial(n + j) / (sp.factorial(n) * n**j)
        total += term
    return sp.together(sp.simplify(phi(K) / 4**K * total))


targets = {
    1: (4 * n + 1) / (6 * n),
    2: (8 * n**2 + 4 * n + 1) / (15 * n**2),
    3: (64 * n**3 + 48 * n**2 + 25 * n + 6) / (140 * n**3),
    4: (128 * n**4 + 128 * n**3 + 103 * n**2 + 52 * n + 12) / (315 * n**4),
}

print("=== R1: Corolario A1 vs independently-PROVED closed forms ===\n")

all_pass = True
for K, target in targets.items():
    mine = psi_closed_form(K)
    diff = sp.simplify(mine - target)
    ok = (diff == 0)
    all_pass = all_pass and ok
    print(f"K={K}: match={ok}  (diff simplifies to {diff})")
    print(f"   mine   = {sp.factor(mine)}")
    print(f"   target = {sp.factor(target)}")

# K=5: only cross-check the 1/n^2 coefficient against the archive's stated
# value 1405/2772 (full closed form not transcribed here, avoid silently
# copying an untranscribed target). Extract via series in 1/n.
K = 5
mine5 = psi_closed_form(K)
h = sp.symbols('h', positive=True)  # h = 1/n
mine5_h = mine5.subs(n, 1 / h)
series5 = sp.series(mine5_h, h, 0, 4).removeO()
coeff_h2 = series5.coeff(h, 2)
target_h2 = sp.Rational(1405, 2772)
ok5 = sp.simplify(coeff_h2 - target_h2) == 0
all_pass = all_pass and ok5
print(f"\nK=5: 1/n^2 coefficient = {coeff_h2}, target = {target_h2}, match={ok5}")

# Also check phi_K limit (n -> infinity) matches phi_K for K=1..8, and the
# K=0 degenerate case psi_n^{(0)} == 1 identically.
print("\n=== limit check: psi_n^{(K)} -> phi_K as n -> oo, K=0..8 ===")
for K in range(0, 9):
    mine = psi_closed_form(K)
    lim = sp.limit(mine, n, sp.oo)
    target = sp.simplify(phi(K))
    ok = sp.simplify(lim - target) == 0
    all_pass = all_pass and ok
    print(f"K={K}: lim={lim}, phi_K={target}, match={ok}")

K0 = psi_closed_form(0)
ok0 = sp.simplify(K0 - 1) == 0
all_pass = all_pass and ok0
print(f"\npsi_n^{{(0)}} == 1 identically: {sp.simplify(K0)}  match={ok0}")

print(f"\n=== ALL R1 CHECKS PASS: {all_pass} ===")
