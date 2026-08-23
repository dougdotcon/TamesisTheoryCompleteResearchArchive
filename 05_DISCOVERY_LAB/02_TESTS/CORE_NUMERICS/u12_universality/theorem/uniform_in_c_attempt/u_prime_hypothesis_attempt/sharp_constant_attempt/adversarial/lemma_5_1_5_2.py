"""
Independent re-verification of Lemma 5.1 (termwise P_j >= h(j)) and
Lemma 5.2 (h decreasing), from scratch. Does NOT read the target's own
verify_Q_lower_bound.py.

P_j := prod_{i=1}^j (1 - i/n),   h(j) := exp(-j(j+1)/(2(n-j)))
"""
import mpmath as mp
from fractions import Fraction as F

mp.mp.dps = 60

def P_j_sequence(n):
    """Yield P_0, P_1, ..., P_{n-1} incrementally (O(n) multiplications, not O(n^2))."""
    p = F(1)
    yield p
    for i in range(1, n):
        p *= F(n - i, n)
        yield p

def h_mp(n, j):
    n = mp.mpf(n); j = mp.mpf(j)
    return mp.e**(-(j*(j+1))/(2*(n-j)))

# --- Part 0: the elementary inequality -ln(1-x) <= x/(1-x), x in [0,1) ---
print("=== Part 0: elementary inequality -ln(1-x) <= x/(1-x) ===")
bad = 0
xs = [mp.mpf(k)/1000 for k in range(0, 1000)]  # x in [0, 0.999]
for x in xs:
    lhs = -mp.log(1-x)
    rhs = x/(1-x)
    if lhs > rhs + mp.mpf('1e-50'):
        bad += 1
        print("VIOLATION at x=", x, lhs, rhs)
print(f"checked {len(xs)} points in [0,0.999], violations={bad}")
# also very close to 1
xs2 = [1 - mp.mpf(10)**(-k) for k in range(1, 30)]
bad2 = 0
for x in xs2:
    lhs = -mp.log(1-x)
    rhs = x/(1-x)
    if lhs > rhs + mp.mpf('1e-40'):
        bad2 += 1
        print("VIOLATION near 1 at x=", x)
print(f"checked {len(xs2)} points approaching x->1, violations={bad2}")

# --- Part 1: termwise P_j >= h(j), exact Fraction P_j vs mpmath h(j) ---
print("\n=== Part 1: termwise P_j >= h(j) (exact P_j vs mpmath h(j), 60dps) ===")
ns = [1,2,3,5,10,20,50,100,300,1000,3000,10000]
total = 0
violations = 0
worst_margin = None
for n in ns:
    for j, Pj in enumerate(P_j_sequence(n)):
        Pj_mp = mp.mpf(Pj.numerator)/mp.mpf(Pj.denominator)
        hj = h_mp(n, j)
        total += 1
        margin = Pj_mp - hj
        if margin < -mp.mpf('1e-45'):
            violations += 1
            print(f"VIOLATION n={n} j={j}: P_j={Pj_mp} h(j)={hj}")
        if worst_margin is None or margin < worst_margin[0]:
            worst_margin = (margin, n, j)
print(f"checked {total} (n,j) pairs across n in {ns}, violations={violations}")
print(f"worst (smallest) margin P_j-h(j) = {worst_margin}")

# --- Part 1b: much larger n, pure mpmath log-sum (stress test, not exact) ---
print("\n=== Part 1b: termwise P_j >= h(j), large n, mpmath log-sum (stress test) ===")
bad1b = 0
tot1b = 0
worst1b = None
for n in [50000, 300000, 1000000]:
    n_mp = mp.mpf(n)
    log_p = mp.mpf(0)
    # sample j sparsely (checking all j for n=10^6 is 10^6 mpmath calls; do all,
    # it's O(n) and mpmath at 60dps handles this in well under a minute)
    for j in range(0, n):
        if j >= 1:
            log_p += mp.log(1 - mp.mpf(j)/n_mp)
        Pj_mp = mp.e**log_p
        hj = h_mp(n, j)
        tot1b += 1
        margin = Pj_mp - hj
        if margin < -mp.mpf('1e-30'):
            bad1b += 1
            if bad1b <= 5:
                print(f"VIOLATION n={n} j={j}: P_j={Pj_mp} h(j)={hj}")
        if worst1b is None or margin < worst1b[0]:
            worst1b = (margin, n, j)
    print(f"  n={n} done, cumulative checked={tot1b}, violations so far={bad1b}")
print(f"large-n stress test: checked {tot1b} (n,j) pairs, violations={bad1b}")
print(f"worst (smallest) margin (large-n) = {worst1b}")

# --- Part 2: Lemma 5.2, h(x) strictly decreasing on [0,n) ---
print("\n=== Part 2: h(x) strictly decreasing on [0,n) ===")
bad3 = 0
tot3 = 0
for n in [5, 20, 100, 1000, 10000]:
    xs = [mp.mpf(n)*k/2000 for k in range(0, 2000)]  # 0 .. n*1999/2000, strictly < n
    prev = None
    for x in xs:
        val = h_mp(n, x) if x != int(x) else h_mp(n, int(x))
        # use continuous version directly
        n_ = mp.mpf(n)
        val = mp.e**(-(x*(x+1))/(2*(n_-x)))
        tot3 += 1
        if prev is not None and val >= prev:
            bad3 += 1
            print(f"MONOTONICITY VIOLATION n={n} around x={x}")
        prev = val
print(f"checked {tot3} points across several n, monotonicity violations={bad3}")

# --- Part 2b: symbolic sign check of phi'(x) numerator ---
print("\n=== Part 2b: symbolic check that phi'(x) numerator > 0 on [0,n) ===")
import sympy as sp
x, n = sp.symbols('x n', positive=True)
phi = x*(x+1)/(2*(n-x))
phi_prime = sp.diff(phi, x)
phi_prime_simplified = sp.simplify(phi_prime)
# claimed numerator: (2x+1)(n-x) + x(x+1), over 2(n-x)^2
claimed_num = (2*x+1)*(n-x) + x*(x+1)
claimed_phi_prime = claimed_num / (2*(n-x)**2)
diff = sp.simplify(phi_prime - claimed_phi_prime)
print("phi'(x) - claimed_phi'(x) simplifies to:", diff, " (should be 0)")
# expand the claimed numerator fully
print("claimed numerator (2x+1)(n-x)+x(x+1) expanded:", sp.expand(claimed_num))
