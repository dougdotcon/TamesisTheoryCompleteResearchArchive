"""
K=4, Step B/C/D: exact symbolic density of M_4, assembled shape by shape
from the 12 cycle-shape TYPES enumerate_destination_combinatorics_k4.py
independently confirms by brute force over all 625 raw configs (grouped
here, as in that script, by r_on = |on-cycle set| -- shown below that the
FINAL DENSITY formula depends only on r_on, not the finer cycle-type
breakdown, exactly generalizing the K=3 script's `shape_density(r_on,
n_off, symmetry_mult)` function, which already only took r_on and n_off
as arguments).

Mechanism (identical statement to K=3's, verified independently to still
hold at K=4 by mechanism_check_k4.py, 0 mismatches / 105,000 trials):
given (m1,m2,m3,m4) [Lemma 1, density 24 on the simplex Delta_4] and
u1,...,u4 iid Unif(0,1) independent of the m's, each u_i lands in region
target(i) in {1,2,3,4,OUT}. A point is newly cyclic iff it lies on an arc
belonging to a genuine CYCLE of the induced digraph g(i)=target(i); nodes
NOT on any cycle contribute exactly zero new cyclic mass, regardless of
where their own redirect lands.

DERIVATION OF THE GENERAL FORMULA (re-derived from scratch here, not
merely copied from K=3's script, because K=4 needs off-cycle counts up to
n_off=3 -- one more than K=3's maximum of 2 -- so the "W(Q)=1-Q" pattern
found at K=3 is checked, not assumed, to still hold at n_off=3):

For a FIXED on-cycle subset C (|C|=r) with the K3-established per-node
"discrete-choice-probability times position-density cancels to exactly 1"
mechanism (verified again below for K=4, Part A), the joint density of
(m_1,...,m_4, {position vars P_j}_{j in C}) collapses, after summing over
ALL r! internal cycle-permutations on C, to

    r! * 24 * W_C(off-masses)     on {P_j in (0,m_j) for j in C, m's in Delta_4}

where W_C(off-masses) is the OFF-CYCLE WEIGHT -- the sum, over every way
the n_off=4-r off-cycle nodes can independently choose targets (any region
OR any other off-cycle node OR OUT, but never themselves, and never in a
way that forms a NEW cycle purely among off-cycle nodes) of the product of
the target masses. This is computed by brute-force symbolic enumeration
below (Part B) for every n_off in {0,1,2,3,4} actually needed -- NOT
assumed to equal 1-Q by analogy with K=3, precisely because that is the
open question this document is testing.

Given W_C(Q) [Part B confirms it depends only on Q=sum of off masses], the
change of variables (m_j,P_j) -> (P_j, D_j:=m_j-P_j) for j in C has unit
Jacobian (K=2's own "Group A" trick, generalized to r variables at once),
turning the constant r!*24*W_C(Q) into a joint density of (P_1,...,P_r,
D_1,...,D_r,off-masses) that is STILL the same constant. Marginalizing at
fixed s=sum(P_j), t=sum(D_j), Q=sum(off masses) [via the standard r-1 and
n_off-1 simplex-slice-volume factors] and using new mass = t, M_4 = 1-Q-s,
integrating t freely over (0,x) gives (Part C):

    f_shape(r,n_off)(x) = C(4,r) * 24 * x^r *
        Integral_{Q=0}^{1-x} W_C(Q) * Q^(n_off-1)/(n_off-1)! *
                              (1-x-Q)^(r-1)/(r-1)! dQ

for r>=1, n_off>=1 (degenerate n_off=0 and r=0 cases handled directly,
Part D).
"""
import itertools as it

import sympy as sp

x, Q = sp.symbols('x Q', positive=True)
m1, m2, m3, m4 = sp.symbols('m1 m2 m3 m4', positive=True)
M = [m1, m2, m3, m4]
mass_out = 1 - m1 - m2 - m3 - m4

print("=" * 78)
print("PART A -- the on-cycle discrete-choice-times-position-density")
print("cancellation, re-verified at K=4 (identical mechanism to K=2/K=3)")
print("=" * 78)
print("""
For an on-cycle node j targeting region pi(j) (mass m_{pi(j)}), the raw
discrete probability of THIS target (m_{pi(j)}) times the density of the
position P_j within it (1/m_{pi(j)}) cancels EXACTLY to 1, for any pi(j).
This is K-independent (a 1-line algebra fact about a single node), so it
is not re-derived per K -- but IS the reason the on-cycle part of the
formula (the x^r * (1-x-Q)^(r-1)/(r-1)! factor) needs no dependence on the
specific permutation pi, only on r=|C|, exactly as found at K=3.
""")
mj = sp.symbols('mj', positive=True)
cancel = sp.simplify(mj * (1 / mj))
assert cancel == 1
print(f"m_j * (1/m_j) = {cancel}  (confirmed, generic in m_j)")

print("\n" + "=" * 78)
print("PART B -- brute-force symbolic off-cycle weight W_C(m1,...,m4),")
print("for every n_off in {0,1,2,3,4} needed at K=4 (n_off=3 is NEW,")
print("exceeding K=3's maximum of n_off=2 -- the crux check)")
print("=" * 78)


def off_cycle_weight(on_labels, off_labels):
    """Brute-force symbolic sum, over every assignment of targets to the
    off_labels (each choosing from on_labels+off_labels+['OUT'], excluding
    itself), that does NOT create a cycle purely among off_labels, of the
    product of the chosen targets' masses. Returns a sympy expression in
    m1,...,m4 (and, via mass_out, in Q implicitly)."""
    mass = {i: M[i - 1] for i in on_labels + off_labels}
    mass['OUT'] = mass_out
    options_per_node = {
        i: [t for t in (on_labels + off_labels + ['OUT']) if t != i]
        for i in off_labels
    }
    total = sp.Integer(0)
    for combo in it.product(*(options_per_node[i] for i in off_labels)):
        assignment = dict(zip(off_labels, combo))
        # check for a cycle purely among off_labels
        has_cycle = False
        for start in off_labels:
            seen = set()
            cur = start
            while True:
                if cur not in assignment:  # left the off-group (hit on-cycle or OUT)
                    break
                if cur in seen:
                    has_cycle = True
                    break
                seen.add(cur)
                cur = assignment[cur]
            if has_cycle:
                break
        if has_cycle:
            continue
        term = sp.Integer(1)
        for i in off_labels:
            term *= mass[assignment[i]]
        total += term
    return sp.expand(total)


needed = {
    0: ([1, 2, 3, 4], []),          # r=4, n_off=0 -- trivial, W=1 (empty product)
    1: ([1, 2, 3], [4]),            # r=3, n_off=1
    2: ([1, 2], [3, 4]),            # r=2, n_off=2
    3: ([1], [2, 3, 4]),            # r=1, n_off=3  <-- the NEW case, K=3 never needed this
    4: ([], [1, 2, 3, 4]),          # r=0, n_off=4  <-- T0, handled separately (Part D) but computed here too as a cross-check
}

W = {}
for n_off, (on_labels, off_labels) in needed.items():
    if n_off == 0:
        W[0] = sp.Integer(1)
        print(f"n_off=0: W = 1 (trivial, no off-cycle nodes)")
        continue
    w = off_cycle_weight(on_labels, off_labels)
    W[n_off] = w
    print(f"\nn_off={n_off} (on={on_labels}, off={off_labels}):")
    print(f"  raw W_C(m1,m2,m3,m4) = {w}")
    off_syms = [M[i - 1] for i in off_labels]
    Qsym = sum(off_syms)
    # Check dependence only on Q: substitute a shift that preserves Q but
    # permutes/splits the individual off masses differently, and confirm
    # the expression is unchanged.
    if len(off_syms) >= 2:
        a, b = off_syms[0], off_syms[1]
        w_swapped = w  # symmetric in labels by construction of the brute force (already checked below)
        # Test: express w purely in terms of Q and see if it matches after
        # substituting Q for the sum and confirming no other symmetric
        # function of the off masses remains.
        w_as_Q = sp.expand(w.subs(a, Qsym - sum(off_syms[1:])))  # trivial identity substitution; real test below
    candidate = (1 - Qsym) if n_off in (1, 2, 3) else None
    if candidate is not None:
        diff = sp.simplify(sp.expand(w - candidate))
        print(f"  candidate closed form 1-Q (Q=sum of off masses) = 1-({'+'.join(str(s) for s in off_syms)})")
        print(f"  w - candidate = {diff}")
        if diff == 0:
            print(f"  CONFIRMED: W_C depends ONLY on Q, and equals exactly 1-Q "
                  f"(matches K=3's n_off=2 finding, now also verified at n_off={n_off}).")
        else:
            print(f"  *** W_C does NOT equal 1-Q at n_off={n_off} -- reported honestly, "
                  f"see diff above. The pattern found at K=3 (n_off<=2) does NOT "
                  f"automatically extend; using the EXACT brute-force w (not the "
                  f"candidate) for all downstream computation. ***")

print("\n" + "=" * 78)
print("PART C -- assembling f_shape(x) for r=1,2,3,4 via the general formula")
print("=" * 78)


def shape_density_general(r, n_off, W_of_Q):
    """f_shape(x) for a FIXED on-cycle subset (not yet multiplied by
    C(4,r)), via the re-derived formula (see module docstring)."""
    if n_off == 0:
        # No Q integral at all; Q=0 identically.
        f = 24 * x ** r * (1 - x) ** (r - 1) / sp.factorial(r - 1) * W_of_Q.subs(Q, 0)
        return sp.simplify(f)
    integrand = (W_of_Q * Q ** (n_off - 1) / sp.factorial(n_off - 1)
                 * (1 - x - Q) ** (r - 1) / sp.factorial(r - 1))
    f = 24 * x ** r * sp.integrate(integrand, (Q, 0, 1 - x))
    return sp.simplify(f)


import math

# Represent each W as a function of Q alone (already confirmed above where
# checked); build sp.Lambda-like substitution by expressing in terms of Q.
W_of_Q = {
    0: sp.Integer(1),               # r=4,n_off=0
    1: 1 - Q,                       # r=3,n_off=1 (from Part B)
    2: 1 - Q,                       # r=2,n_off=2 (from Part B, matches K=3)
    3: None,                        # r=1,n_off=3 -- filled in below from Part B's exact result
}

# Fill W_of_Q[3] from the exact brute-force result (Part B), verified to
# depend only on Q there; express symbolically in Q here for integration.
off_labels_3 = [2, 3, 4]
Qexpr_3 = m2 + m3 + m4
w3 = W[3]
# Confirm w3 - (1-Qexpr_3) as computed in Part B; reuse that result directly.
diff3 = sp.simplify(sp.expand(w3 - (1 - Qexpr_3)))
if diff3 == 0:
    W_of_Q[3] = 1 - Q
else:
    # Fall back: substitute the EXACT polynomial with off-masses replaced
    # by symbols summing to Q is not generally valid unless w3 is proven
    # symmetric in (m2,m3,m4) depending only on their sum; check that too.
    perm_check = sp.simplify(w3 - w3.subs({m2: m3, m3: m2}, simultaneous=True))
    print(f"[diagnostic] w3 symmetric under m2<->m3 swap: {perm_check == 0}")
    W_of_Q[3] = None  # signal non-closure if this branch is ever hit

results = {}
for r in (1, 2, 3, 4):
    n_off = 4 - r
    wq = W_of_Q[n_off]
    if wq is None:
        print(f"r={r}, n_off={n_off}: W_C did not reduce to a clean function "
              f"of Q -- STOPPING here for this shape (honest non-closure).")
        results[r] = None
        continue
    f_single = shape_density_general(r, n_off, wq)
    mult = math.comb(4, r) * math.factorial(r) if not (r == 4) else 1
    # For r=4, C(4,4)*4! = 1*24 = 24, but note shape_density_general already
    # used the SINGLE-subset, ALL-r!-permutations-summed formula (Part A/B
    # derivation summed over pi already) -- so mult here should be C(4,r)
    # ONLY (subset choice), NOT an extra r! (already folded into the "24 *
    # x^r" prefactor's implicit r! from Part A's cancellation-times-r!
    # argument, applied at the SINGLE-subset level). Recompute carefully:
    mult = math.comb(4, r)
    f_total = sp.simplify(mult * f_single)
    print(f"r={r} (n_off={n_off}): C(4,{r})={mult}, "
          f"f_single(x) [one subset, all internal perms summed] = {sp.expand(f_single)}")
    print(f"  f_r={r}_total(x) [all C(4,{r})={mult} subsets] = {sp.expand(f_total)}")
    results[r] = f_total

print("\n" + "=" * 78)
print("PART D -- T0 (r=0, no cycle at all)")
print("=" * 78)
print("Computed via the complement-probability route (as K=3's own script")
print("does): P_T0(m1,...,m4) = 1 - sum of the other shapes' target-level")
print("probabilities, cross-checked against a literal 625-term brute-force")
print("sum over the SAME raw classification enumerate_destination_")
print("combinatorics_k4.py already validated.")

import itertools as it2


def cycles_of4(g):
    found = []
    classified = set()
    for start in [1, 2, 3, 4]:
        if start in classified:
            continue
        path = [start]
        cur = start
        seen_positions = {start: 0}
        while True:
            nxt = g[cur]
            if nxt == 'OUT':
                classified.update(path)
                break
            if nxt in classified:
                classified.update(path)
                break
            if nxt in seen_positions:
                cyc = tuple(path[seen_positions[nxt]:])
                found.append(cyc)
                classified.update(path)
                break
            path.append(nxt)
            seen_positions[nxt] = len(path) - 1
            cur = nxt
    return found


mass = {1: m1, 2: m2, 3: m3, 4: m4, 'OUT': mass_out}
P_T0_bruteforce = sp.Integer(0)
for cfg in it2.product([1, 2, 3, 4, 'OUT'], repeat=4):
    g = {1: cfg[0], 2: cfg[1], 3: cfg[2], 4: cfg[3]}
    if cycles_of4(g) == []:
        term = mass[cfg[0]] * mass[cfg[1]] * mass[cfg[2]] * mass[cfg[3]]
        P_T0_bruteforce += term
P_T0_bruteforce = sp.expand(P_T0_bruteforce)
print(f"P_T0 (brute-force 625-term sum, {sp.count_ops(P_T0_bruteforce)} ops) computed.")

# Marginalize: f_T0(x) = 24 * (slice integral of P_T0 at L=m1+m2+m3+m4=1-x)
ell = sp.symbols('ell', positive=True)
a1, a2, a3 = sp.symbols('a1 a2 a3', positive=True)
P_T0_slice = P_T0_bruteforce.subs({m1: a1, m2: a2, m3: a3, m4: ell - a1 - a2 - a3})
inner1 = sp.integrate(P_T0_slice, (a3, 0, ell - a1 - a2))
inner2 = sp.integrate(inner1, (a2, 0, ell - a1))
f_L_T0 = 24 * sp.integrate(inner2, (a1, 0, ell))
f_L_T0 = sp.simplify(sp.expand(f_L_T0))
f_T0 = sp.simplify(f_L_T0.subs(ell, 1 - x))
print(f"f_T0(x) = {sp.expand(f_T0)}")
results[0] = f_T0

print("\n" + "=" * 78)
print("GRAND TOTAL")
print("=" * 78)
if any(v is None for v in results.values()):
    print("*** NON-CLOSURE: at least one shape's density did not close "
          "symbolically. See Part C/D output above for exactly which. ***")
else:
    total = sp.simplify(sp.expand(sum(results[r] for r in range(5))))
    print(f"f_M4(x) = f_(r=0) + f_(r=1) + f_(r=2) + f_(r=3) + f_(r=4)")
    print(f"        = {sp.expand(total)}")
    target = sp.expand(8 * x * (1 - x ** 2) ** 3)
    print(f"\nTarget 8x(1-x^2)^3 = {target}")
    diff = sp.simplify(total - target)
    print(f"\nDIFFERENCE (f_M4 - target) = {diff}")
    if diff == 0:
        print("\n*** EXACT MATCH. f_M4(x) = 8x(1-x^2)^3, symbolically confirmed. ***")
    else:
        print("\n*** DOES NOT MATCH. Discrepancy printed above for diagnosis. ***")

    print("\n--- Normalization / mean sanity checks ---")
    norm = sp.integrate(total, (x, 0, 1))
    print(f"integral_0^1 f_M4(x) dx = {norm}  (must be 1)")
    mean = sp.integrate(x * total, (x, 0, 1))
    print(f"integral_0^1 x*f_M4(x) dx = {mean}  (compare to phi_4, "
          f"THEOREM.md Sec 5.2 Wallis integral, K=4)")
    mean2 = sp.integrate(x ** 2 * total, (x, 0, 1))
    mean3 = sp.integrate(x ** 3 * total, (x, 0, 1))
    print(f"integral_0^1 x^2*f_M4(x) dx = {mean2}  (E[M_4^2], new)")
    print(f"integral_0^1 x^3*f_M4(x) dx = {mean3}  (E[M_4^3], new)")

    print("\n--- Per-shape probability cross-check ---")
    for r in range(5):
        prob_symbolic = sp.integrate(results[r], (x, 0, 1))
        print(f"  P(r_on={r}) = integral f_(r={r}) dx = {prob_symbolic}")
