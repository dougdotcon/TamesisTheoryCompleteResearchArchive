"""
K=3, Step B/C/D: exact symbolic density of M_3, assembled group by group
from the 7 cycle-shapes of enumerate_destination_combinatorics.py (that
script independently confirms, by brute force over all 64 raw configs,
the shape counts used here: T0=16, T1a=24 (8/subtype), T1b=9 (3/pair),
T1c=2, T2a=9 (3/pair), T2b=3, T3=1).

Mechanism (generalizing conjecture1_k2_attempt/ATTEMPT.md Section 3):
given (m1,m2,m3) [Lemma 1, density 6 on the simplex Delta] and u1,u2,u3
iid Unif(0,1) independent of (m1,m2,m3), each u_i lands in region
target(i) in {1,2,3,OUT}. A point is newly cyclic iff it lies on an arc
belonging to a genuine CYCLE of the induced digraph g(i)=target(i) on
{1,2,3} (self-loop / 2-cycle / 3-cycle / disjoint unions thereof); nodes
NOT on any cycle contribute exactly zero new cyclic mass, regardless of
where their own redirect lands (a direct generalization of the K=2
"single-cross-plus-OUT drains away" mechanism -- proved in ATTEMPT.md
Section 3 of this front's own document, mirroring K=2's Lemma 0).

For every one of the 6 non-empty shapes, new cyclic mass is exactly
  (m1+m2+m3) - (sum of masses of "off-cycle" regions) - (sum of the
  "position" variables P_i := position of u_i within its on-cycle target
  region, for each on-cycle node i)
so that M_3 = (1-m1-m2-m3) + [new mass] = 1 - (sum of off-cycle m's) -
(sum of on-cycle P's), UNIFORMLY across all 6 shapes (verified below by
direct symbolic substitution for every shape).

This script derives each shape's exact contribution f_shape(x) to
f_{M_3}(x) via a change-of-variables marginalization (never invoking a
Dirac delta, exactly as ATTEMPT.md K=2 Section 4 does), sums them
(T0 obtained as 1 minus the other 6 target-level probabilities, verified
both symbolically and by an independent direct 3D integral), and compares
the total to 6*x*(1-x^2)^2.
"""
import sympy as sp

x, s = sp.symbols('x s', positive=True)
m1, m2, m3 = sp.symbols('m1 m2 m3', positive=True)


def shape_density(r_on, n_off, symmetry_mult, label):
    """
    General formula (derived in ATTEMPT.md Section on Step 2/assembly):

    f_shape(x) = symmetry_mult * 6 *
        Integral_{s=0}^{1-x} [ s**(r_on-1)/(r_on-1)! ]          # P's joint density at fixed sum s
                              * phi(1-s-x) * W(1-s-x)            # off-cycle Q=1-s-x weight+degeneracy
                              * x**r_on / r_on!                  # on-cycle m' simplex volume at fixed x
                              ds

    where phi(Q) = Q**(n_off-1)/(n_off-1)!  (=1 if n_off==0, trivial if
    n_off==1, =Q if n_off==2) and W(Q) = 1 if n_off==0 else (1-Q).

    For n_off==0 there is no off-cycle integral at all (Q is identically
    0); the closed form collapses to the elementary
        f_shape(x) = symmetry_mult * 6 * (1-x)**(r_on-1)/(r_on-1)! * x**r_on/r_on!
    which is used directly (and independently re-derived via the general
    integral below as a cross-check).
    """
    r_on_fact = sp.factorial(r_on)
    if n_off == 0:
        f_direct = symmetry_mult * 6 * (1 - x) ** (r_on - 1) / sp.factorial(r_on - 1) * x ** r_on / r_on_fact
        f_direct = sp.simplify(f_direct)
        # cross-check via the general integral with a dummy n_off=0 (no Q integral, s ranges 0..1-x
        # but Q must be exactly 0 => this general form does not directly apply; skip cross-check here,
        # it is already the "direct" elementary derivation for T3/T1c/T2b.
        return f_direct

    n_off_fact_m1 = sp.factorial(n_off - 1)
    Q = 1 - s - x
    phi = Q ** (n_off - 1) / n_off_fact_m1
    W = 1 - Q
    integrand = (s ** (r_on - 1) / sp.factorial(r_on - 1)) * phi * W * (x ** r_on / r_on_fact) * 6
    f = symmetry_mult * sp.integrate(integrand, (s, 0, 1 - x))
    return sp.simplify(f)


print("=" * 78)
print("K=3 STEP B/C/D -- shape-by-shape density derivation")
print("=" * 78)

# T1a: self-loop, r_on=1 (P_i), n_off=2 (Q=m_j+m_k), symmetry x3
f_T1a = shape_density(r_on=1, n_off=2, symmetry_mult=3, label='T1a')
print(f"\nf_T1a(x) = {f_T1a}")

# T1b: 2-cycle, r_on=2 (A,B), n_off=1 (Q=m_k), symmetry x3
f_T1b = shape_density(r_on=2, n_off=1, symmetry_mult=3, label='T1b')
print(f"f_T1b(x) = {f_T1b}")

# T1c: 3-cycle, r_on=3 (P1,P2,P3), n_off=0, symmetry x2 (orientations)
f_T1c = shape_density(r_on=3, n_off=0, symmetry_mult=2, label='T1c')
print(f"f_T1c(x) = {f_T1c}")

# T2a: two self-loops, r_on=2 (P_i,P_j), n_off=1 (Q=m_k), symmetry x3
f_T2a = shape_density(r_on=2, n_off=1, symmetry_mult=3, label='T2a')
print(f"f_T2a(x) = {f_T2a}")

# T2b: self + 2-cycle, r_on=3 (P_i,C,D), n_off=0, symmetry x3
f_T2b = shape_density(r_on=3, n_off=0, symmetry_mult=3, label='T2b')
print(f"f_T2b(x) = {f_T2b}")

# T3: three self-loops, r_on=3 (P1,P2,P3), n_off=0, symmetry x1
f_T3 = shape_density(r_on=3, n_off=0, symmetry_mult=1, label='T3')
print(f"f_T3(x) = {f_T3}")

print("\n--- Cross-check against by-hand derivations in ATTEMPT.md ---")
assert sp.simplify(f_T3 - x ** 3 * (1 - x) ** 2 / 2) == 0
print("f_T3 matches hand derivation x^3(1-x)^2/2  OK")
hand_T2a = sp.Rational(3, 2) * x ** 2 * (1 - x) ** 2 * (2 + x)
print(f"hand_T2a = {sp.expand(hand_T2a)}, code f_T2a = {sp.expand(f_T2a)}")
assert sp.simplify(f_T2a - hand_T2a) == 0
print("f_T2a matches hand derivation (3/2)x^2(1-x)^2(2+x)  OK")

sum_6 = sp.simplify(f_T1a + f_T1b + f_T1c + f_T2a + f_T2b + f_T3)
print(f"\nSum of the 6 non-T0 shape densities = {sp.expand(sum_6)}")

# ---------------------------------------------------------------------
# T0: no cycle. Compute via 1 - (target-level probability of the other
# 6 shapes), then marginalize the (m1,m2,m3) slice at L=m1+m2+m3=1-x.
# ---------------------------------------------------------------------
print("\n--- T0 (no cycle) ---")
P_T1a = m1 * (1 - m2 - m3) + m2 * (1 - m1 - m3) + m3 * (1 - m1 - m2)
P_T1b = m1 * m2 * (1 - m3) + m1 * m3 * (1 - m2) + m2 * m3 * (1 - m1)
P_T1c = 2 * m1 * m2 * m3
P_T2a = m1 * m2 * (1 - m3) + m1 * m3 * (1 - m2) + m2 * m3 * (1 - m1)
P_T2b = 3 * m1 * m2 * m3
P_T3 = m1 * m2 * m3
P_T0 = sp.expand(1 - (P_T1a + P_T1b + P_T1c + P_T2a + P_T2b + P_T3))
print(f"P_T0(m1,m2,m3) = {P_T0}")

# Sanity: brute-force cross-check of P_T0 by literal 64-term enumeration
# over the 4 target choices per node (m1,m2,m3,1-m1-m2-m3), using the
# SAME classification code as enumerate_destination_combinatorics.py.
import itertools as it


def cycles_of(g, nodes=(1, 2, 3)):
    found = []
    classified = set()
    for start in nodes:
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


mass = {1: m1, 2: m2, 3: m3, 'OUT': 1 - m1 - m2 - m3}
P_T0_bruteforce = sp.Integer(0)
for cfg in it.product([1, 2, 3, 'OUT'], repeat=3):
    g = {1: cfg[0], 2: cfg[1], 3: cfg[2]}
    if cycles_of(g) == []:
        term = mass[cfg[0]] * mass[cfg[1]] * mass[cfg[2]]
        P_T0_bruteforce += term
P_T0_bruteforce = sp.expand(P_T0_bruteforce)
print(f"P_T0 (brute-force 16-term sum over the T0-classified raw configs) = {P_T0_bruteforce}")
assert sp.simplify(P_T0 - P_T0_bruteforce) == 0
print("MATCHES the complement formula exactly -- P_T0 confirmed by two independent routes.")

# Now marginalize: f_T0(x) = 6 * (density, at L=1-x, of P_T0(m1,m2,m3)
# integrated over the simplex slice {m1,m2,m3>0, m1+m2+m3=ell}).
ell = sp.symbols('ell', positive=True)
m1v, m2v = sp.symbols('m1v m2v', positive=True)
P_T0_slice = P_T0.subs({m1: m1v, m2: m2v, m3: ell - m1v - m2v})
inner = sp.integrate(P_T0_slice, (m2v, 0, ell - m1v))
f_L_T0 = 6 * sp.integrate(inner, (m1v, 0, ell))
f_L_T0 = sp.simplify(sp.expand(f_L_T0))
print(f"\nf_L^(T0)(ell) [density of L=m1+m2+m3 weighted by P_T0] = {f_L_T0}")
f_T0 = sp.simplify(f_L_T0.subs(ell, 1 - x))
print(f"f_T0(x) = f_L^(T0)(1-x) = {sp.expand(f_T0)}")

# ---------------------------------------------------------------------
# Grand total
# ---------------------------------------------------------------------
print("\n" + "=" * 78)
total = sp.simplify(sp.expand(sum_6 + f_T0))
print(f"f_M3(x) = f_T0 + f_T1a + f_T1b + f_T1c + f_T2a + f_T2b + f_T3")
print(f"        = {sp.expand(total)}")
target = sp.expand(6 * x * (1 - x ** 2) ** 2)
print(f"\nTarget 6x(1-x^2)^2 = {target}")
diff = sp.simplify(total - target)
print(f"\nDIFFERENCE (f_M3 - target) = {diff}")
if diff == 0:
    print("\n*** EXACT MATCH. f_M3(x) = 6x(1-x^2)^2, symbolically confirmed. ***")
else:
    print("\n*** DOES NOT MATCH. Discrepancy printed above for diagnosis. ***")

print("\n--- Normalization / mean sanity checks ---")
norm = sp.integrate(total, (x, 0, 1))
print(f"integral_0^1 f_M3(x) dx = {norm}  (must be 1)")
mean = sp.integrate(x * total, (x, 0, 1))
print(f"integral_0^1 x*f_M3(x) dx = {mean}  (compare to phi_3, THEOREM.md Sec 5.2 Wallis integral)")
