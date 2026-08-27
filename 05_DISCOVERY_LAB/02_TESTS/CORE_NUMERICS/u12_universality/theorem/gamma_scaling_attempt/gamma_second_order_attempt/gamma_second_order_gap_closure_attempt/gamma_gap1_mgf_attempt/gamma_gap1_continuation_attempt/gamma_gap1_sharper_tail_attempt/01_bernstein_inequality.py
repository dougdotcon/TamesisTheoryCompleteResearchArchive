"""
GAMMA-GAP1-SHARPER-TAIL-ATTEMPT, script 01.

Derive, from scratch (elementary calculus only, no external library import,
no archive .py file read), the classical Bernstein inequality for a sum of
k i.i.d. centered Bernoulli(gamma) variables, and independently verify it
against the EXACT Binomial tail probability (mpmath dps=50, direct pmf
summation -- no shortcuts), across a wide grid of (k, gamma, t).

Setup (cited from required reading): M ~ Bin(k,gamma), D := M - gamma*k.
Write D = sum_{i=1}^k Y_i, Y_i i.i.d., Y_i = Bernoulli(gamma) - gamma, taking
value (1-gamma) with probability gamma and -gamma with probability (1-gamma).
  sigma^2 := Var(Y_i) = gamma(1-gamma)          (exact)
  M_bound := max(gamma, 1-gamma) >= |Y_i| a.s.  (exact, sharp)

CLASSICAL FACT (Bernstein's inequality for bounded random variables; see e.g.
S. Bernstein 1946 / Boucheron-Lugosi-Massart "Concentration Inequalities"
(2013) Thm 2.10, cited at the same tier this lineage already cites Hoeffding's
inequality). We give the full elementary derivation below for completeness
and independent verification, since the whole point of this front is to
audit whether a non-Hoeffding tail-control technique is legitimately sharper
here -- not to take a citation on faith.

  P(|D| > t) <= 2*exp( -t^2 / (2*k*sigma^2 + (2/3)*M_bound*t) )    for all t>0.

Derivation (short, elementary, self-contained):
  1. For |Y|<=M, E[Y]=0: for integer j>=2, E[Y^j] <= M^{j-2} E[Y^2] = M^{j-2} sigma^2
     (since |Y|^j = |Y|^{j-2} Y^2 <= M^{j-2} Y^2 pointwise).
  2. Hence for lambda>0: E[e^{lambda Y}] = 1 + sum_{j>=2} lambda^j E[Y^j]/j!
       <= 1 + (sigma^2/M^2) * sum_{j>=2} (lambda M)^j / j!
        = 1 + (sigma^2/M^2)*(e^{lambda M} - 1 - lambda M)
       <= exp[ (sigma^2/M^2)*(e^{lambda M} - 1 - lambda M) ]        (1+x<=e^x)
     -- this is Bennett's MGF bound (classical).
  3. Elementary calculus fact:  e^u - 1 - u <= (u^2/2)/(1 - u/3)  for 0<=u<3.
     (Proof: both sides are power series in u with the same u^0,u^1 terms
     zero; comparing coefficients of u^j, j>=2: LHS has 1/j!, RHS has
     1/(2*3^{j-2}); 2*3^{j-2} <= j! holds for every j>=2 by an elementary
     induction (equality at j=2,3; then j!/(j-1)! = j > 3 for j>=4 while the
     RHS ratio is exactly 3), so termwise LHS <= RHS.)
  4. Substituting u=lambda*M (0<=lambda<3/M) into steps 2-3:
       E[e^{lambda Y}] <= exp[ sigma^2*lambda^2 / (2*(1-lambda*M/3)) ].
  5. For the sum D of k i.i.d. copies, V:=k*sigma^2:
       E[e^{lambda D}] <= exp[ V*lambda^2 / (2*(1-lambda*M/3)) ],  0<=lambda<3/M.
  6. Chernoff/Markov: P(D>=t) <= exp[ V*lambda^2/(2*(1-lambda*M/3)) - lambda*t ].
     Minimizing over lambda (standard calculus, optimal lambda*=t/(V+Mt/3))
     gives P(D>=t) <= exp(-t^2/(2V+2Mt/3)). Two-sided by symmetry of the
     argument (apply to -Y_i too): P(|D|>=t) <= 2*exp(-t^2/(2V+2Mt/3)).

This script verifies step 3 and the final inequality (step 6) independently,
numerically, against the exact Binomial tail.
"""
import mpmath as mp

mp.mp.dps = 50


def exact_tail_prob(k, gam, t):
    """P(|Bin(k,gam) - gam*k| > t), exact via direct pmf summation."""
    gam = mp.mpf(gam)
    k = int(k)
    total = mp.mpf(0)
    for j in range(0, k + 1):
        D = j - gam * k
        if abs(D) > t:
            pmf = mp.binomial(k, j) * gam ** j * (1 - gam) ** (k - j)
            total += pmf
    return total


def hoeffding_bound(k, t):
    return 2 * mp.e ** (-2 * t ** 2 / k)


def bernstein_bound(k, gam, t):
    gam = mp.mpf(gam)
    sigma2 = gam * (1 - gam)
    M = max(gam, 1 - gam)
    denom = 2 * k * sigma2 + mp.mpf(2) / 3 * M * t
    if denom == 0:
        return mp.mpf(2) if t == 0 else mp.mpf(0)
    return 2 * mp.e ** (-(t ** 2) / denom)


print("=" * 78)
print("PART A: elementary calculus fact  e^u-1-u <= (u^2/2)/(1-u/3), 0<=u<3")
print("=" * 78)
max_viol = mp.mpf(0)
checked = 0
for i in range(1, 300):  # u = 0.01 .. 2.99, step 0.01
    u = mp.mpf(i) / 100
    lhs = mp.e ** u - 1 - u
    rhs = (u ** 2 / 2) / (1 - u / 3)
    checked += 1
    if lhs > rhs:
        max_viol = max(max_viol, lhs - rhs)
print(f"checked {checked} points in (0,3); max violation (lhs>rhs, should be 0): {max_viol}")
assert max_viol == 0

print()
print("=" * 78)
print("PART B: Bernstein bound is a valid upper bound on the EXACT tail prob")
print("=" * 78)
violations = 0
checked = 0
worst_ratio = mp.mpf(0)
for k in [5, 20, 50, 200, 1000]:
    for gam_f in [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
        for Cfac in [1.0, 2.0, 3.0, 5.0]:
            t = mp.mpf(Cfac) * mp.sqrt(mp.mpf(k) * mp.log(1000))
            if t > k:
                continue
            exact = exact_tail_prob(k, gam_f, t)
            bern = bernstein_bound(k, gam_f, t)
            checked += 1
            if exact > bern + mp.mpf('1e-45'):
                violations += 1
                print("VIOLATION (Bernstein)", k, gam_f, Cfac, exact, bern)
            if bern > 0:
                worst_ratio = max(worst_ratio, exact / bern)
print(f"checked={checked} violations={violations}")
print(f"worst (exact tail)/(Bernstein bound) ratio (must be <=1): {worst_ratio}")
assert violations == 0

print()
print("=" * 78)
print("PART C: Bernstein vs Hoeffding bound, fixed (k,t), across gamma")
print("(illustrates that Bernstein is dramatically sharper away from gamma=1/2,")
print(" and matches/loses only very near gamma=1/2 where sigma^2=1/4 is exactly")
print(" the value Hoeffding implicitly assumes for every gamma)")
print("=" * 78)
n_val = 10 ** 6
k_val = 5000
C_val = 3.0
t_val = mp.mpf(C_val) * mp.sqrt(mp.mpf(k_val) * mp.log(n_val))
for gam_f in [0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]:
    bern = bernstein_bound(k_val, gam_f, t_val)
    hoef = hoeffding_bound(k_val, t_val)
    ratio = bern / hoef
    print(f"gamma={gam_f:>5}: bernstein={mp.nstr(bern, 6):>14}  hoeffding={mp.nstr(hoef, 6):>14}  "
          f"ratio(Bernstein/Hoeffding)={mp.nstr(ratio, 6)}")

print()
print("All checks passed. Bernstein's inequality (derived from scratch above)")
print("is confirmed valid against exact Binomial tails with zero violations,")
print("and is confirmed dramatically sharper than Hoeffding away from gamma=1/2.")
