#!/usr/bin/env python3
"""
INDEPENDENT symbolic re-derivation of Proposicao D2's closed form.

No .py file from any front in this lineage was read. This script starts
from the same raw combinatorial facts stated in ATTEMPT.md's prose
(Sec 2-4: the arc/tail mechanics, Proposicao S, the conditional CDF via
paircount) -- already independently re-confirmed from scratch elsewhere
in this adversarial/ directory (prop_s_symbolic.py,
position_level_reference.py) -- but performs the FINAL symbolic
double/triple summation that assembles Proposicao D2 using a DIFFERENT
method than ATTEMPT.md's own "shift trick" (s := v+w): here PairAgg is
derived by directly swapping summation order on the raw (L0, v, w) triple
sum via sympy, term by term, not via the s-substitution shortcut. This is
an independent proof of the same closed form, not a re-typing of the
front's derivation.

Also symbolically checks the "single regime, no separate boundary case"
claim (ATTEMPT.md Sec 4.2): that regime (i)'s formula, evaluated
symbolically at k = n-1, equals the value obtained from directly summing
Contribution(O) over the FULL boundary range O=0..n-2 (regime (ii)) --
done here by re-deriving regime (ii) totally independently too (not
merely substituting into regime (i)'s already-derived formula).
"""
import sympy as sp

n, k, O, L0, t, m, v, w = sp.symbols('n k O L0 t m v w', positive=True)

print("=" * 70)
print("Step 1: PairAgg(m,t) := sum_{L0=1}^{m-1} paircount(L0, m-L0, t)")
print("Independent derivation via raw (L0,v,w) triple-sum order swap")
print("(NOT the front's s=v+w 'shift trick').")
print("=" * 70)

# paircount(L0, m-L0, t) = #{(v,w): 1<=v<=L0, 1<=w<=m-L0, v+w<=t}
# Sum over L0=1..m-1 of that count = #{(L0,v,w): 1<=L0<=m-1, 1<=v<=L0,
#   1<=w<=m-L0, v+w<=t}.
# Swap order: fix (v,w) with v,w>=1, v+w<=t. For which L0 in [1,m-1] do
# we have v<=L0 and L0<=m-w? That's L0 in [v, m-w] (nonempty exactly
# when v<=m-w, i.e. v+w<=m -- guaranteed since v+w<=t<=m in the regime
# used later). Count of such L0 = (m-w) - v + 1 = m - v - w + 1.
# So PairAgg(m,t) = sum_{v=1}^{t-1} sum_{w=1}^{t-v} (m - v - w + 1).
inner = sp.summation(m - v - w + 1, (w, 1, t - v))
inner = sp.expand(inner)
pairagg_derived = sp.summation(inner, (v, 1, t - 1))
pairagg_derived = sp.simplify(sp.expand(pairagg_derived))
print(f"  Derived PairAgg(m,t) = {pairagg_derived}")

pairagg_claimed = t * (3 * m * t - 3 * m - 2 * t**2 + 3 * t - 1) / 6
diff = sp.simplify(pairagg_derived - pairagg_claimed)
print(f"  Claimed (ATTEMPT.md Sec 4.1) PairAgg(m,t) = {pairagg_claimed}")
print(f"  diff = {diff}   {'OK' if diff == 0 else 'MISMATCH'}")
assert diff == 0, "PairAgg closed form MISMATCH"

# Numeric cross-check of the derived closed form against a direct O(m)
# recomputation, for many (m,t) -- independent of the symbolic algebra.
print()
print("  Numeric cross-check of derived PairAgg formula vs direct O(m) "
      "double loop, m=2..25, all valid t:")


def paircount_raw(A, B, tt):
    if tt < 2:
        return 0
    total = 0
    for vv in range(1, min(A, tt - 1) + 1):
        wmax = min(B, tt - vv)
        if wmax >= 1:
            total += wmax
    return total


def pairagg_raw(mm, tt):
    return sum(paircount_raw(L0v, mm - L0v, tt) for L0v in range(1, mm))


n_checks = 0
all_ok = True
pairagg_fn = sp.lambdify((m, t), pairagg_derived, 'math')
for mm in range(2, 26):
    for tt in range(0, mm + 1):
        raw = pairagg_raw(mm, tt)
        formula = pairagg_fn(mm, tt)
        n_checks += 1
        if round(formula) != raw:
            all_ok = False
            print(f"    MISMATCH m={mm} t={tt}: raw={raw} formula={formula}")
print(f"  {n_checks} numeric comparisons, "
      f"{'ALL MATCH' if all_ok else 'MISMATCH FOUND'}")
assert all_ok

print()
print("=" * 70)
print("Step 2: S1(t,m,O,n) := sum_{L0=1}^{m-1} (L0+O)/n^2 * clip(t,0,L0)")
print("Independent derivation via direct split at L0=t (clip=min(t,L0)")
print("since t>=0), summing each piece with sympy directly.")
print("=" * 70)

# clip(t,0,L0) = min(t, L0) for t>=0. Split range L0=1..m-1 at L0=t:
#   L0 = 1..t-1 : contributes L0 (the smaller of t,L0)
#   L0 = t..m-1 : contributes t
# (valid whenever 1 <= t <= m-1, which ATTEMPT.md Sec 4.2 claims always
#  holds in the regime used -- verified independently in Step 3 below).
piece1 = sp.summation((L0 + O) / n**2 * L0, (L0, 1, t - 1))
piece2 = sp.summation((L0 + O) / n**2 * t, (L0, t, m - 1))
s1_derived = sp.simplify(sp.expand(piece1 + piece2))
print(f"  Derived S1(t,m,O,n) = {s1_derived}")

s1_claimed = t * (6 * O * m - 3 * O * t - 3 * O + 3 * m**2 - 3 * m
                   - t**2 + 1) / (6 * n**2)
diff2 = sp.simplify(s1_derived - s1_claimed)
print(f"  Claimed (ATTEMPT.md Sec 4.1) S1(t,m,O,n) = {s1_claimed}")
print(f"  diff = {diff2}   {'OK' if diff2 == 0 else 'MISMATCH'}")
assert diff2 == 0, "S1 closed form MISMATCH"

# Numeric cross-check.
print()
print("  Numeric cross-check of derived S1 formula vs direct O(m) loop, "
      "several (n,O), all valid (m,t):")


def s1_raw(tt, mm, Ov, nn):
    total = sp.Rational(0)
    for L0v in range(1, mm):
        cl = min(tt, L0v) if tt >= 0 else 0
        total += sp.Rational(L0v + Ov, nn**2) * cl
    return total


s1_fn = sp.lambdify((t, m, O, n), s1_derived, 'math')
n_checks2 = 0
all_ok2 = True
for nn in (6, 9, 13, 17):
    for Ov in range(0, nn - 1):
        mm = nn - Ov
        if mm < 2:
            continue
        for tt in range(0, mm):
            raw = s1_raw(tt, mm, Ov, nn)
            formula = sp.Rational(s1_fn(tt, mm, Ov, nn)).limit_denominator(10**9)
            n_checks2 += 1
            if sp.simplify(raw - formula) != 0:
                all_ok2 = False
                print(f"    MISMATCH n={nn} O={Ov} m={mm} t={tt}: "
                      f"raw={raw} formula={formula}")
print(f"  {n_checks2} numeric comparisons, "
      f"{'ALL MATCH' if all_ok2 else 'MISMATCH FOUND'}")
assert all_ok2

print()
print("=" * 70)
print("Step 3: is t <= m-1 always true in the range used (so Step 2's "
      "split is well-posed with no further sub-casing)?")
print("=" * 70)
# t = k-O, m = n-O. Claim: for 0<=O<=min(k,n-2), 0<=k<=n-1: t <= m-1.
# t <= m-1  <=>  k-O <= n-O-1  <=>  k <= n-1.  This holds by hypothesis
# (k<=n-1) UNCONDITIONALLY, for every O -- confirmed here symbolically,
# not just asserted.
claim_expr = sp.simplify((n - O - 1) - (k - O))  # m-1 - t
print(f"  (m-1) - t = {claim_expr}  (independent of O, as expected)")
print(f"  This is >= 0 exactly when k <= n-1, which is the assumed "
      f"domain -- CONFIRMED, t<=m-1 holds unconditionally in-domain.")

print()
print("=" * 70)
print("Step 4: assemble Contribution(O) and sum over O -- regime (i), "
      "0<=k<=n-2, O=0..k.")
print("=" * 70)

t_sub = k - O
m_sub = n - O
contribution = ((m_sub - 1) * (O / n)
                 + 2 * s1_derived.subs({t: t_sub, m: m_sub})
                 + sp.Rational(2) / n**2 * pairagg_derived.subs({t: t_sub, m: m_sub}))
contribution = sp.simplify(sp.expand(contribution))
print(f"  Contribution(O) [before the O<=k Iverson bracket -- trivially "
      f"true throughout this regime's O range] = {contribution}")

F_regime_i_raw = sp.summation(contribution, (O, 0, k))
F_regime_i = sp.simplify(sp.factor(sp.Rational(2, 1) / (n * (n - 1)) * F_regime_i_raw))
print(f"  F_regime_i(k) [derived, INDEPENDENT summation order] = {F_regime_i}")

F_claimed_i = -k * (k + 1) * (k**2 - k - 2 * n**2 + 3 * n) / (n**3 * (n - 1))
diff3 = sp.simplify(F_regime_i - F_claimed_i)
print(f"  Claimed regime-(i) formula (ATTEMPT.md Sec 4.2) = {F_claimed_i}")
print(f"  diff = {diff3}   {'OK' if diff3 == 0 else 'MISMATCH'}")
assert diff3 == 0, "Regime (i) closed form MISMATCH"

D2_target = k * (k + 1) * (2 * n**2 - 3 * n + k - k**2) / (n**3 * (n - 1))
diff3b = sp.simplify(F_regime_i - D2_target)
print(f"  vs Proposicao D2's headline formula = {D2_target}")
print(f"  diff = {diff3b}   {'OK' if diff3b == 0 else 'MISMATCH'}")
assert diff3b == 0

print()
print("=" * 70)
print("Step 5: independently derive regime (ii) (k=n-1, O=0..n-2) FROM "
      "SCRATCH (not by substituting into regime (i)'s already-derived "
      "formula) and compare to regime (i) evaluated at k=n-1.")
print("=" * 70)

# For k = n-1 directly: t = (n-1) - O, m = n - O. Independent summation.
kk = n - 1
t_sub2 = kk - O
contribution2 = ((m_sub - 1) * (O / n)
                  + 2 * s1_derived.subs({t: t_sub2, m: m_sub})
                  + sp.Rational(2) / n**2 * pairagg_derived.subs({t: t_sub2, m: m_sub}))
contribution2 = sp.simplify(sp.expand(contribution2))
F_regime_ii_raw = sp.summation(contribution2, (O, 0, n - 2))
F_regime_ii = sp.simplify(sp.factor(sp.Rational(2, 1) / (n * (n - 1)) * F_regime_ii_raw))
print(f"  F_regime_ii (independently derived, O summed 0..n-2 directly) "
      f"= {F_regime_ii}")

F_boundary_claimed = (n**2 - 2) / n**2
diff4 = sp.simplify(F_regime_ii - F_boundary_claimed)
print(f"  Claimed regime-(ii) formula = {F_boundary_claimed}")
print(f"  diff = {diff4}   {'OK' if diff4 == 0 else 'MISMATCH'}")
assert diff4 == 0

F_regime_i_at_boundary = sp.simplify(F_regime_i.subs(k, n - 1))
diff5 = sp.simplify(F_regime_i_at_boundary - F_regime_ii)
print(f"  F_regime_i(k=n-1) = {F_regime_i_at_boundary}")
print(f"  F_regime_ii (independently derived) = {F_regime_ii}")
print(f"  diff = {diff5}   "
      f"{'OK -- single formula genuinely covers k=n-1 too' if diff5 == 0 else 'MISMATCH -- boundary case IS needed, contradicting the single-regime claim'}")
assert diff5 == 0

print()
print("ALL STEPS PASSED: Proposicao D2's closed form is independently "
      "re-derived from raw first principles (different summation order "
      "than the front's own 'shift trick'), and the single-regime "
      "(no separate k=n-1 boundary case) claim is independently "
      "confirmed by deriving regime (ii) from scratch, not merely by "
      "substituting into regime (i)'s own formula.")
