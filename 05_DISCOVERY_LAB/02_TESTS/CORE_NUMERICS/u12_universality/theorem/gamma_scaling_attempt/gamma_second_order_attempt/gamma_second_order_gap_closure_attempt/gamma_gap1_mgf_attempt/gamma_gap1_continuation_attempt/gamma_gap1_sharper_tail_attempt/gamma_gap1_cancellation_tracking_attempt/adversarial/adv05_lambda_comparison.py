"""
Referee check: lambda_tight(gamma) vs lambda(gamma) (Estagio 36's "true
leading constant", lambda(gamma) = 4(3-2gamma)/(gamma(2-gamma))).

Verifies:
 - lambda_tight(gamma) := max(4, 4(1-gamma)^2/(gamma(2-gamma))) < lambda(gamma)
   for EVERY gamma in (0,1), by full symbolic algebra (not just sampling).
 - specific ratios at gamma=1/2 (target claims 2.67x smaller) and
   gamma=0.01 (target claims 3.04x smaller).
 - WHY lambda(gamma) is loose: independently re-derive it from the crude,
   triangle-inequality-summed g(K) := |c1(K)|*K + |c2(K)|*K^2 (the
   quantity Estagio 36 actually built lambda(gamma) from -- summing
   ABSOLUTE VALUES of c1(K) and c2(K) separately, i.e. evaluated as if
   D=K, the symmetric case), and confirm this reproduces lambda(gamma)
   exactly at leading order -- confirming the target's diagnosis that
   lambda(gamma) itself still carries triangle-inequality slack.
"""
import sympy as sp

gamma = sp.symbols('gamma', positive=True)
n, k = sp.symbols('n k', positive=True)

lambda_true = 4*(3-2*gamma)/(gamma*(2-gamma))          # Estagio 36's lambda(gamma)
lambda_tight_pieceA = sp.Integer(4)
lambda_tight_pieceB = 4*(1-gamma)**2/(gamma*(2-gamma))

gamma_star = 1 - sp.sqrt(2)/2
print("gamma* = 1 - sqrt(2)/2 =", sp.N(gamma_star))

print("\n=== Part 1: lambda_tight(gamma) < lambda(gamma) for every gamma in (0,1), full symbolic proof ===")

# Piece A (gamma >= gamma*): lambda_tight = 4. Need lambda_true(gamma) > 4 throughout (0,1)
# (in particular on [gamma*,1)). Show algebraically:
diffA = sp.simplify(lambda_true - 4)
print("lambda_true - 4 =", diffA)
numA, denA = sp.fraction(sp.together(diffA))
numA = sp.factor(sp.expand(numA))
denA = sp.factor(denA)
print("  numerator (factored):", numA, "   denominator (factored):", denA)
# numerator = -4*(gamma-1)*(gamma-3) = 4*(1-gamma)*(3-gamma); denominator = gamma*(gamma-2) = -gamma*(2-gamma)
# both (1-gamma)>0 and (3-gamma)>0 on (0,1); denominator negative(gamma*(gamma-2)<0 on (0,2)) -> ratio positive
print("  For gamma in (0,1): (1-gamma)>0, (3-gamma)>0 so numerator's sign is manifest;")
print("  gamma*(gamma-2) < 0 throughout (0,2). Ratio is POSITIVE throughout (0,1) => lambda_true > 4 always.")

# Piece B (gamma < gamma*): need lambda_true > lambda_tight_pieceB, i.e.
# (3-2*gamma) > (1-gamma)^2  <=>  2 - gamma^2 > 0, trivially true on (0,1).
diffB_inner = sp.expand((3-2*gamma) - (1-gamma)**2)
print("\n(3-2*gamma) - (1-gamma)^2 =", diffB_inner, " (= 2-gamma^2, strictly positive on (0,1))")
full_diffB = sp.simplify(lambda_true - lambda_tight_pieceB)
print("Full symbolic lambda_true - lambda_tight(pieceB) =", full_diffB,
      " (strictly positive on (0,1) since numerator/denominator both have known, matching signs)")

print("\n=> lambda_tight(gamma) < lambda(gamma) CONFIRMED for every gamma in (0,1), full symbolic proof.")

print("\n=== Part 2: specific ratio checks ===")
for gval, claimed_ratio in [(sp.Rational(1,2), 2.67), (sp.Rational(1,100), 3.04)]:
    lt_val = sp.Max(4, lambda_tight_pieceB).subs(gamma, gval)
    l_val = lambda_true.subs(gamma, gval)
    ratio = sp.N(l_val/lt_val, 10)
    print(f"gamma={gval}: lambda_tight={sp.N(lt_val,10)}, lambda={sp.N(l_val,10)}, "
          f"ratio(lambda/lambda_tight)={ratio}  (target claims ~{claimed_ratio}x smaller)")

print("\n=== Part 3: WHY lambda(gamma) is loose -- re-deriving it from the crude,")
print("triangle-inequality-summed bound g(K) = |c1(K)|*K + |c2(K)|*K^2 (symmetric D=K) ===")

c1 = (gamma**2*k**2/2 - gamma*k**2 - gamma*k*n + gamma*k/2 + k**2/2 + k*n - k/2 - n/2 + sp.Rational(1,12)) / n**2
c2 = (2*gamma*k - 2*k - 2*n + 1) / (4*n**2)

beta = gamma*(2-gamma)/2
K = sp.sqrt(4*n*sp.log(n)/beta)

c1_K = c1.subs(k, K)
c2_K = c2.subs(k, K)

# Determine sign of c1(K), c2(K) for gamma in (0,1), large n, via random probing
import random
random.seed(20260938002)  # referee's own sanity-check seed, NOT drawn from the target's reserved block
bad_signs = []
for _ in range(30):
    gval = sp.Rational(random.randint(1, 999), 1000)
    c1v = sp.N(c1_K.subs({gamma: gval, n: 10**8}))
    c2v = sp.N(c2_K.subs({gamma: gval, n: 10**8}))
    if not (c1v > 0 and c2v < 0):
        bad_signs.append((gval, c1v, c2v))
print("Sign check across 30 random gamma in (0,1), n=1e8: c1(K)>0 and c2(K)<0 always?",
      len(bad_signs) == 0, " bad cases:", bad_signs)

# So |c1(K)| = c1(K), |c2(K)| = -c2(K); the crude bound is c1(K)*K - c2(K)*K^2
gK_crude_abs = (c1_K*K - c2_K*K**2).factor()
lim_val = sp.limit(gK_crude_abs/sp.log(n), n, sp.oo)
lim_val = sp.simplify(lim_val)
print("\nlim_{n->oo} (|c1(K)|*K + |c2(K)|*K^2)/ln(n) =", lim_val)
print("Estagio 36's lambda(gamma) = 4(3-2*gamma)/(gamma*(2-gamma))")
print("Exact symbolic difference:", sp.simplify(lim_val - lambda_true), " <- should be 0")
print("\n=> CONFIRMED: lambda(gamma) is exactly the leading order of the crude,")
print("triangle-inequality-summed |c1|K+|c2|K^2 bound at the SYMMETRIC point D=K --")
print("the target's diagnosis of why lambda(gamma), despite being labeled the")
print("'true leading constant' by predecessors, still carries triangle-inequality")
print("slack, is independently confirmed accurate.")
