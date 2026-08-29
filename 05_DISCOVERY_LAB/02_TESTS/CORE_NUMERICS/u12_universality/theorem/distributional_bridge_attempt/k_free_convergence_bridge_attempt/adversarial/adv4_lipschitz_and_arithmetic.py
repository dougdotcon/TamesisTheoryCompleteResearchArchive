"""
Independent verification of Section 6:
  - the Lipschitz-constant lemma for f_K(x) = 2*K*x*(1-x^2)^(K-1):
      maximizer x* = 1/sqrt(2K-1)
      Lambda_K = [2K/sqrt(2K-1)] * [(2K-2)/(2K-1)]^(K-1)
      Lambda_K <= 2*sqrt(K)
  - the final assembled arithmetic:
      delta(K,n) + Lambda_K * eps(K,n) <= 8 K^2 / n
    where delta(K,n) = (3K^2-K)/(2n), eps(K,n) = (2K+1)/n.
"""
import sympy as sp
import math

K, x = sp.symbols('K x', positive=True)

print("=== Part 1: critical point of f_K(x) = 2Kx(1-x^2)^(K-1) ===")
Kval_list = [1, 2, 3, 5, 10, 20, 50, 100]
all_ok = True
for Kv in Kval_list:
    xs = sp.symbols('xs', positive=True)
    fK = 2 * Kv * xs * (1 - xs**2) ** (Kv - 1)
    dfK = sp.diff(fK, xs)
    xstar_claimed = 1 / sp.sqrt(2 * Kv - 1)
    if Kv == 1:
        # K=1: f_1(x)=2x is strictly increasing on [0,1] (derivative
        # constant =2, no interior critical point) -- the "critical point"
        # x*=1/sqrt(2*1-1)=1 is the boundary maximizer, degenerate case of
        # the general formula, not an interior stationary point. Handle
        # separately rather than mis-flagging findroot's failure as an error.
        cval = 1.0
    else:
        # find critical point in (0,1) symbolically/numerically
        crit = sp.solve(sp.Eq(dfK, 0), xs)
        crit_real = [c for c in crit if c.is_real and 0 < c < 1]
        if crit_real:
            cval = float(crit_real[0])
        else:
            f_np = sp.lambdify(xs, dfK, 'mpmath')
            import mpmath
            cval = float(mpmath.findroot(f_np, 0.5))
    xstar_val = float(xstar_claimed)
    ok = abs(cval - xstar_val) < 1e-9
    all_ok = all_ok and ok
    # value of Lambda_K at critical point vs formula
    Lambda_direct = float(fK.subs(xs, xstar_claimed))
    Lambda_formula = (2 * Kv / math.sqrt(2 * Kv - 1)) * ((2 * Kv - 2) / (2 * Kv - 1)) ** (Kv - 1) if Kv > 1 else (2*Kv/math.sqrt(2*Kv-1))*1.0
    ok2 = abs(Lambda_direct - Lambda_formula) < 1e-9
    bound_ok = Lambda_direct <= 2 * math.sqrt(Kv) + 1e-12
    all_ok = all_ok and ok2 and bound_ok
    print(f"K={Kv:>4}  x*_solve={cval:.8f}  x*_claimed={xstar_val:.8f}  match={ok}   "
          f"Lambda_direct={Lambda_direct:.6f}  Lambda_formula={Lambda_formula:.6f}  match={ok2}   "
          f"2sqrt(K)={2*math.sqrt(Kv):.6f}  Lambda<=2sqrtK: {bound_ok}")
print("ALL Lipschitz-lemma checks pass:", all_ok)
print()

print("=== Part 1b: is x* really a MAXIMUM (not min/inflection)? Check f'' sign / direct grid scan ===")
all_ok_max = True
for Kv in [1, 2, 3, 5, 10, 20]:
    xs_grid = [i / 200000 for i in range(1, 200000)]
    fK = lambda xv: 2 * Kv * xv * (1 - xv**2) ** (Kv - 1)
    vals = [fK(xv) for xv in xs_grid]
    max_val = max(vals)
    max_x = xs_grid[vals.index(max_val)]
    xstar = 1 / math.sqrt(2 * Kv - 1)
    lam = (2 * Kv / math.sqrt(2 * Kv - 1)) * ((2 * Kv - 2) / (2 * Kv - 1)) ** (Kv - 1) if Kv > 1 else 2.0
    ok = abs(max_x - xstar) < 2e-4 and abs(max_val - lam) < 2e-4
    all_ok_max = all_ok_max and ok
    print(f"K={Kv:>3}  grid-argmax x={max_x:.6f} (claimed x*={xstar:.6f})  grid-max f={max_val:.6f} "
          f"(claimed Lambda={lam:.6f})  match={ok}")
print("Grid-scan confirms x* is the true global max on [0,1]:", all_ok_max)
print()

print("=== Part 2: final assembled arithmetic bound delta(K,n)+Lambda_K*eps(K,n) <= 8K^2/n ===")
all_ok_final = True
for Kv in [1, 2, 3, 5, 10, 50, 100, 1000]:
    lam = (2 * Kv / math.sqrt(2 * Kv - 1)) * ((2 * Kv - 2) / (2 * Kv - 1)) ** (Kv - 1) if Kv > 1 else 2.0
    lam_bound = 2 * math.sqrt(Kv)
    n_test = 1  # bound should hold as a coefficient-of-1/n inequality; test with n factored out
    delta_coef = (3 * Kv**2 - Kv) / 2.0   # delta(K,n) = delta_coef / n
    eps_coef = (2 * Kv + 1)               # eps(K,n) = eps_coef / n
    # exact Lambda_K used:
    lhs_exact = delta_coef + lam * eps_coef
    # using the claimed relaxation Lambda_K <= 2 sqrt(K):
    lhs_relaxed = delta_coef + lam_bound * eps_coef
    rhs = 8 * Kv**2
    ok_exact = lhs_exact <= rhs + 1e-9
    ok_relaxed = lhs_relaxed <= rhs + 1e-9
    all_ok_final = all_ok_final and ok_exact and ok_relaxed
    print(f"K={Kv:>5}  [delta_coef + Lambda_K*eps_coef] = {lhs_exact:>14.4f}   "
          f"[with Lambda<=2sqrtK relaxation] = {lhs_relaxed:>14.4f}   8K^2 = {rhs:>10}   "
          f"exact<=8K^2: {ok_exact}   relaxed<=8K^2: {ok_relaxed}")
print("ALL final-arithmetic checks pass (both exact Lambda_K and the 2sqrt(K) relaxation):", all_ok_final)
print()

print("=== Part 2b: symbolic re-derivation of the final inequality's algebra ===")
# delta_coef + 2 sqrt(K) * eps_coef = (3K^2-K)/2 + 2 sqrt(K) * (2K+1)
#                                    = (3K^2-K)/2 + 4 K^1.5 + 2 sqrt(K)
# claim: K^1.5 <= K^2 and sqrt(K) <= K^2 for K>=1, so bracket <= 1.5K^2+4K^2+2K^2=7.5K^2<=8K^2
Kv_sym = sp.symbols('Kv', positive=True)
bracket = sp.Rational(3,2)*Kv_sym**2 - sp.Rational(1,2)*Kv_sym + 4*Kv_sym**sp.Rational(3,2) + 2*Kv_sym**sp.Rational(1,2)
for Kv in [1, 2, 3, 5, 10, 100]:
    bval = float(bracket.subs(Kv_sym, Kv))
    ok = bval <= 8*Kv**2 + 1e-9
    print(f"K={Kv:>4}  bracket(exact)={bval:>12.4f}  7.5K^2={7.5*Kv**2:>10.2f}  8K^2={8*Kv**2:>10}  bracket<=8K^2: {ok}")
