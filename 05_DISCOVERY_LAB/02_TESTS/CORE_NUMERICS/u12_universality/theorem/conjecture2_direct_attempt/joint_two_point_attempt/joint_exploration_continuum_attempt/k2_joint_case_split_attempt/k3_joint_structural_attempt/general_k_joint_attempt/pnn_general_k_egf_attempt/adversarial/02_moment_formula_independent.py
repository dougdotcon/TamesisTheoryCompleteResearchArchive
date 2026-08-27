"""
Independent, from-scratch re-derivation of the symbolic-(n,K,r) composition
moment machinery (target ATTEMPT.md Sec 2.2/5.1), via the Eulerian-
polynomial / ordinary-generating-function approach described in prose
(predecessor Sec 8.4's hint; target Sec 5.1's own description of how it
built its machinery: "computed here by repeated application of the
operator t d/dt to 1/(1-t)"). No .py file from any front was read.

Moment being derived, in general:

  mu(specials=[a_1,...,a_s], r, b; n, K) :=
      sum over compositions L_0,...,L_{K-1} >= 1, O >= 0, sum(L)+O=n  of
          L_0^{a_1} * L_1^{a_2} * ... * L_{s-1}^{a_s}     (s "special" indices)
        * L_s * L_{s+1} * ... * L_{s+r-1}                  (r "touched", power 1)
        * O^b

(the remaining K-s-r sources are "present but untouched": required L>=1,
weight 1). This is exactly the object the target's mu(L_0^2,r,O^1) etc.
notation refers to (s=1 special index for Pieces B/C, s=2 for Piece D).

Method: standard OGF marking. One variable t marks total composition size.
  - "special" index with power a  -> A_a(t) := sum_{L>=1} L^a t^L
  - "touched" index (power 1)     -> t/(1-t)^2
  - "untouched" index (power 0)   -> t/(1-t)
  - O with power b                -> B_b(t) := sum_{O>=0} O^b t^O
        (B_0 = 1/(1-t); B_b = A_b for b>=1, since the O=0 term vanishes)

A_a(t) is computed by repeatedly applying the operator t*d/dt to t/(1-t)
(elementary calculus -- NOT read from any front's code), and always has
the form t^a*E_a(t)/(1-t)^(a+1) for a polynomial E_a(t) of degree <= a-1;
because E_a has degree bounded independent of K and r, the final
coefficient extraction [t^n] can be written as a FINITE sum (over the fixed
number of terms of E_a) of single binomial coefficients whose upper and
lower arguments are explicit LINEAR expressions in n, K, r -- i.e. genuinely
symbolic in K and r, not just in n. This is what makes the moment formula
below symbolic in (n,K,r) simultaneously.
"""
import sympy as sp
from math import comb, factorial

t = sp.symbols('t')
n, K, r = sp.symbols('n K r', positive=True)


def A_poly(a):
    """Return (t_power, E(t)) such that sum_{L>=1} L^a t^L = t^t_power * E(t) / (1-t)^(a+1),
    with E(t) a polynomial in t. Derived purely by repeated application of
    the operator t*d/dt to t/(1-t). NOTE: for the classical Eulerian
    normalization the leading t-power is always 1 (not a) -- verified by
    hand for a=0,1,2,3 (A_2(t)=t(1+t)/(1-t)^3, A_3(t)=t(1+4t+t^2)/(1-t)^4,
    i.e. always a single explicit power of t out front, times a degree
    (a-1) polynomial E_a(t) with E_a(1)=a!)."""
    expr = t / (1 - t)
    for _ in range(a):
        expr = sp.together(sp.expand(t * sp.diff(expr, t)))
    # expr = A_a(t); normalize to extract E_a(t), leading t power is 1
    Ea = sp.expand(sp.cancel(expr * (1 - t) ** (a + 1) / t))
    Ea = sp.Poly(Ea, t)
    return 1, Ea


def moment_formula_symbolic(specials, r_sym, b, K_sym, n_sym):
    """specials: list of concrete powers a_1,...,a_s (small ints).
    Returns a sympy expression in (n_sym, K_sym, r_sym) for the moment."""
    s = len(specials)
    # numerator polynomial = product of E_{a_i}(t) over specials, times E_b(t) (or 1 if b=0)
    num_poly = sp.Integer(1)
    t_power_base = sp.Integer(0)
    denom_power = sp.Integer(0)
    for a in specials:
        if a == 0:
            # a "special" index with power 0 is just an untouched slot; treat directly
            t_power_base += 1
            denom_power += 1
            continue
        tp, Ea = A_poly(a)
        num_poly = sp.expand(num_poly * Ea.as_expr())
        t_power_base += tp
        denom_power += (a + 1)
    # r touched (power 1 each)
    t_power_base += r_sym
    denom_power += 2 * r_sym
    # K - s - r untouched
    untouched_count = K_sym - s - r_sym
    t_power_base += untouched_count
    denom_power += untouched_count
    # O^b
    if b == 0:
        denom_power += 1
    else:
        tp, Eb = A_poly(b)
        num_poly = sp.expand(num_poly * Eb.as_expr())
        t_power_base += tp
        denom_power += (b + 1)

    num_poly = sp.Poly(sp.expand(num_poly), t) if num_poly != 1 else None
    total = sp.Integer(0)
    if num_poly is None:
        terms = [(0, sp.Integer(1))]
    else:
        terms = [(j[0], c) for j, c in num_poly.terms()]
    for j, c in terms:
        m = n_sym - (t_power_base + j)
        D = denom_power
        total += c * sp.binomial(m + D - 1, D - 1)
    return sp.simplify(total)


def gen_compositions(K, n):
    def rec(prefix, remaining_slots, cap):
        if remaining_slots == 0:
            yield tuple(prefix)
            return
        max_here = cap - (remaining_slots - 1)
        for v in range(1, max_here + 1):
            prefix.append(v)
            yield from rec(prefix, remaining_slots - 1, cap - v)
            prefix.pop()
    yield from rec([], K, n)


def brute_moment(specials, r_touch, b, K, n):
    """Direct enumeration ground truth. specials: list of powers for the
    first len(specials) coordinates; next r_touch coordinates touched
    (power 1); rest untouched (power 0, i.e. just required >=1); O^b."""
    s = len(specials)
    total = 0
    for L in gen_compositions(K, n):
        O = n - sum(L)
        val = 1
        for i, a in enumerate(specials):
            val *= L[i] ** a
        for i in range(s, s + r_touch):
            val *= L[i]
        val *= O ** b
        total += val
    return total


if __name__ == "__main__":
    print("=" * 70)
    print("Symbolic-(n,K,r) moment formula: independent derivation vs brute force")
    print("=" * 70)

    all_ok = True

    # ---- one special index (Piece B/C style: a in {1,2,3}, b in {0,1}) ----
    configs = []
    for a in (1, 2, 3):
        for b in (0, 1, 2):
            for K_val in (4, 5, 6, 7):
                for r_val in range(0, K_val - 1):  # r ranges 0..K-2 (one special slot uses up 1)
                    for n_val in (K_val + 2, K_val + 5):
                        configs.append(("1special", [a], r_val, b, K_val, n_val))

    # ---- two special indices (Piece D style: a1,a2 in {1,2}, b=0) ----
    for a1 in (1, 2):
        for a2 in (1, 2):
            for K_val in (5, 6, 7):
                for r_val in range(0, K_val - 2):
                    for n_val in (K_val + 3,):
                        configs.append(("2special", [a1, a2], r_val, 0, K_val, n_val))

    print(f"Testing {len(configs)} concrete (specials,r,b,K,n) configurations...")
    checked = 0
    for kind, specials, r_val, b, K_val, n_val in configs:
        formula = moment_formula_symbolic(specials, sp.Integer(r_val), b, sp.Integer(K_val), sp.Integer(n_val))
        formula_num = int(formula)
        truth = brute_moment(specials, r_val, b, K_val, n_val)
        ok = (formula_num == truth)
        all_ok &= ok
        checked += 1
        if not ok:
            print(f"  MISMATCH: specials={specials} r={r_val} b={b} K={K_val} n={n_val}: "
                  f"formula={formula_num} truth={truth}")
    print(f"\n{checked}/{checked} configurations checked, ALL MATCH: {all_ok}")

    print("\n" + "=" * 70)
    print("Now verify formula is genuinely SYMBOLIC in K and r simultaneously")
    print("(concrete n, symbolic K,r; substitute concrete K,r afterward and compare)")
    print("=" * 70)
    # mu_r(n,K) = C(n+r,K+r) sanity re-derivation (a=0 special unused; here
    # "1 special power=1" with a=1 IS the r-th touched element itself -- use
    # zero specials, pure r touched, b=0, to match the orchestrator's own
    # already-verified mu_r(n,K)=C(n+r,K+r) fact, as an extra anchor.)
    formula_general = moment_formula_symbolic([], r, 0, K, n)
    print("mu_r(n,K) [0 specials, r touched, b=0], derived symbolically in (n,K,r):")
    print(" ", formula_general)
    target_claim = sp.binomial(n + r, K + r)
    diff = sp.simplify(formula_general - target_claim)
    print("  Compare to C(n+r,K+r):", target_claim, "  diff simplifies to:", diff)
    print("  IDENTICAL:", diff == 0)
    all_ok &= (diff == 0)

    print(f"\nOVERALL MOMENT-FORMULA CHECK: {'PASS' if all_ok else 'FAIL'}")
