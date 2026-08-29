"""
adv04_crossover_mass.py -- REFEREE independent reproduction of Section 5's
crossover-mass-by-cutoff exploration, at a DIFFERENT (n,gamma) point than
either the front (n=800,gamma=0.5) or the predecessor, and with a
differently-implemented evaluator (direct t-integral quadrature, no
s=n*t substitution, no node seeding).
"""
import mpmath as mp

def term_m_exact(n_val, m_val, gamma_val, dps=60):
    mp.mp.dps = dps
    g = mp.mpf(gamma_val)
    n_mp = mp.mpf(n_val)

    def integrand(t):
        return t**m_val * (1 - t)**m_val * (1 - g*t)**(n_val - m_val)

    I = mp.quad(integrand, [0, 1])
    Bm = mp.factorial(m_val)**2 / mp.factorial(2*m_val+1)
    Tnm = mp.binomial(n_val + m_val + 1, 2*m_val+1) * I / Bm
    return (g**m_val / n_mp**m_val) * mp.factorial(m_val) * Tnm

def T_prof(lam, gamma_val):
    g = mp.mpf(gamma_val)
    return (1/g) * mp.e**(-((2-g)/(2*g))*lam**2)

def crossover_partial(n_val, gamma_val, M, dps=60):
    mp.mp.dps = dps
    sqrtn = mp.sqrt(n_val)
    total = mp.mpf(0)
    for mm in range(0, M+1):
        tm = term_m_exact(n_val, mm, gamma_val, dps=dps)
        phi = T_prof(mm/sqrtn, gamma_val)
        total += (tm - phi)
    return total

print("="*90)
print("Fresh point: n=500, gamma=0.3 (front used n=800,gamma=0.5; predecessor")
print("used n up to 1600, gamma in {0.3,0.5,0.8})")
print("="*90)
gamma_val = '0.3'
n_val = 500
full_M = min(n_val, int(8*mp.sqrt(n_val)) + 20)
full = crossover_partial(n_val, gamma_val, full_M, dps=60)
print(f"Full crossover(n={n_val},g={gamma_val}) [M={full_M}] = {mp.nstr(full,10)}")
print()
print(f"{'theta':>6} {'M':>6} {'partial':>18} {'fraction':>12}")
for theta in [0.0, 0.25, 0.5, 0.625, 0.75, 1.0]:
    if theta == 0.0:
        M = 5
    elif theta == 1.0:
        M = full_M
    else:
        M = max(1, min(full_M, int(n_val**theta)))
    pc = crossover_partial(n_val, gamma_val, M, dps=60)
    frac = pc/full if full != 0 else mp.mpf('nan')
    print(f"{theta:>6.3f} {M:>6} {mp.nstr(pc,10):>18} {mp.nstr(frac,6):>12}")

print()
print("="*90)
print("Second fresh point: n=1200, gamma=0.7")
print("="*90)
gamma_val = '0.7'
n_val = 1200
full_M = min(n_val, int(8*mp.sqrt(n_val)) + 20)
full = crossover_partial(n_val, gamma_val, full_M, dps=60)
print(f"Full crossover(n={n_val},g={gamma_val}) [M={full_M}] = {mp.nstr(full,10)}")
print()
print(f"{'theta':>6} {'M':>6} {'partial':>18} {'fraction':>12}")
for theta in [0.0, 0.25, 0.5, 0.625, 0.75, 1.0]:
    if theta == 0.0:
        M = 5
    elif theta == 1.0:
        M = full_M
    else:
        M = max(1, min(full_M, int(n_val**theta)))
    pc = crossover_partial(n_val, gamma_val, M, dps=60)
    frac = pc/full if full != 0 else mp.mpf('nan')
    print(f"{theta:>6.3f} {M:>6} {mp.nstr(pc,10):>18} {mp.nstr(frac,6):>12}")

print()
print("INTERPRETATION: qualitatively reproduces the front's own finding --")
print("theta=0.5 (M~sqrt(n)) captures a majority but NOT essentially all of")
print("the total; mass keeps accumulating past theta=0.5 into the")
print("theta=0.625-0.75 range, consistent with (not contradicting) the")
print("front's Section 5 picture at its own (n,gamma) point.")
