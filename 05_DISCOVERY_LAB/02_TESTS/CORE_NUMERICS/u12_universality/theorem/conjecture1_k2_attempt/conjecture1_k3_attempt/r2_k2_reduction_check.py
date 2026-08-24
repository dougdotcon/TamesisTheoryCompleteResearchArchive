"""
R2 -- K=2 reduction check: apply this front's OWN general method (the
`shape_density` technique of derive_step2_k3_symbolic.py, generalized to
N=2 total reroute sources instead of N=3) and confirm it reproduces
conjecture1_k2_attempt/ATTEMPT.md's already-PROVED result f_{M_2}(x) =
4x(1-x^2) exactly. Mirrors that document's own R2 (which checked its
K=2 method degenerates correctly to the already-proved K=1 result).

Honest process note (reported per this archive's standing discipline of
reporting bugs caught along the way, not silently fixing them): the
FIRST attempt at this reduction, done by hand-enumerating shapes for
N=2 (self-loop-with-other-off x2, one 2-cycle, no-cycle), MISSED the
"both nodes self-loop simultaneously" shape entirely (the N=2 analogue
of K=3's T3) and produced total = 4x - x^2 - 3x^3, which does NOT match
4x(1-x^2) = 4x-4x^3 (diff = x^2(x-1) != 0). This was caught immediately
by the exact-symbolic-match check itself (not silently accepted) and
diagnosed: the missing shape restores the difference exactly. This is
exactly the sort of by-hand miscount this document's Section on Step 2
warns is why the K=3 classification itself was done by *exhaustive
computer enumeration* (enumerate_destination_combinatorics.py) rather
than by hand -- and this very mistake, caught here on the much smaller
N=2 case, is offered as concrete evidence for why that discipline
mattered for the N=3 case treated in the main derivation.
"""
import itertools
import sympy as sp

x, s = sp.symbols('x s', positive=True)


def cycles_of(g, nodes):
    found = []
    classified = set()
    for start in nodes:
        if start in classified:
            continue
        path = [start]
        cur = start
        seen = {start: 0}
        while True:
            nxt = g[cur]
            if nxt == 'OUT':
                classified.update(path)
                break
            if nxt in classified:
                classified.update(path)
                break
            if nxt in seen:
                found.append(tuple(path[seen[nxt]:]))
                classified.update(path)
                break
            path.append(nxt)
            seen[nxt] = len(path) - 1
            cur = nxt
    return found


print("--- Brute-force shape classification for N=2 (3^2=9 raw configs) ---")
nodes = [1, 2]
targets = [1, 2, 'OUT']
shape_counts = {}
for cfg in itertools.product(targets, repeat=2):
    g = {1: cfg[0], 2: cfg[1]}
    cycs = cycles_of(g, nodes)
    key = tuple(sorted(tuple(sorted(c)) for c in cycs))
    shape_counts[key] = shape_counts.get(key, 0) + 1
print(shape_counts, "total =", sum(shape_counts.values()))
assert sum(shape_counts.values()) == 9
print("Confirms 4 shapes: T0(no cycle, 3 configs), self-at-1(2), self-at-2(2),")
print("both-self(1), 2cycle(1) -- 3+2+2+1+1=9. NOTE: 'self-at-1' and 'self-at-2'")
print("are symmetric sub-types of ONE shape ('single self-loop, other node NOT")
print("self-looping'), combined via symmetry_mult=2 below; 'both-self' is a")
print("SEPARATE shape (missed in the first hand-attempt, see module docstring).")

base_density = sp.factorial(2)  # K=2 Lemma-1 density on the segment = 2


def shape_density(r_on, n_off, symmetry_mult):
    r_on_fact = sp.factorial(r_on)
    if n_off == 0:
        return sp.simplify(symmetry_mult * base_density * (1 - x) ** (r_on - 1)
                            / sp.factorial(r_on - 1) * x ** r_on / r_on_fact)
    n_off_fact_m1 = sp.factorial(n_off - 1)
    Q = 1 - s - x
    phi = Q ** (n_off - 1) / n_off_fact_m1
    W = 1 - Q
    integrand = (s ** (r_on - 1) / sp.factorial(r_on - 1)) * phi * W * (x ** r_on / r_on_fact) * base_density
    return sp.simplify(symmetry_mult * sp.integrate(integrand, (s, 0, 1 - x)))


f_self = shape_density(r_on=1, n_off=1, symmetry_mult=2)       # single self-loop, other node off (not self)
f_2cyc = shape_density(r_on=2, n_off=0, symmetry_mult=1)       # 2-cycle
f_bothself = shape_density(r_on=2, n_off=0, symmetry_mult=1)   # BOTH nodes self-loop (the missed shape)
print(f"\nf_self(single self-loop, other off) = {f_self}")
print(f"f_2cyc (the 2-cycle)                = {f_2cyc}")
print(f"f_bothself (both self-loop)         = {f_bothself}")

m1, m2 = sp.symbols('m1 m2', positive=True)
P_T0 = 1 - m1 - m2
ell = sp.symbols('ell', positive=True)
m1v = sp.symbols('m1v', positive=True)
P_T0_slice = P_T0.subs({m1: m1v, m2: ell - m1v})
f_L_T0 = base_density * sp.integrate(P_T0_slice, (m1v, 0, ell))
f_T0 = sp.simplify(f_L_T0.subs(ell, 1 - x))
print(f"f_T0 (no cycle)                     = {f_T0}")

total_WITHOUT_bothself = sp.simplify(f_self + f_2cyc + f_T0)
print(f"\n[first, INCOMPLETE attempt] sum without 'both-self' = {sp.expand(total_WITHOUT_bothself)}")
diff_wrong = sp.simplify(total_WITHOUT_bothself - 4 * x * (1 - x ** 2))
print(f"  diff vs target 4x(1-x^2) = {diff_wrong}  <-- NONZERO, caught the missing shape")

total = sp.simplify(f_self + f_2cyc + f_bothself + f_T0)
print(f"\n[corrected, complete] sum = {sp.expand(total)}")
target = sp.expand(4 * x * (1 - x ** 2))
print(f"target 4x(1-x^2) = {target}")
diff = sp.simplify(total - target)
print(f"diff = {diff}")
assert diff == 0
print("\n*** MATCH. This front's general method, applied to N=2, exactly reproduces ***")
print("*** conjecture1_k2_attempt/ATTEMPT.md's already-proved f_M2(x)=4x(1-x^2).  ***")
