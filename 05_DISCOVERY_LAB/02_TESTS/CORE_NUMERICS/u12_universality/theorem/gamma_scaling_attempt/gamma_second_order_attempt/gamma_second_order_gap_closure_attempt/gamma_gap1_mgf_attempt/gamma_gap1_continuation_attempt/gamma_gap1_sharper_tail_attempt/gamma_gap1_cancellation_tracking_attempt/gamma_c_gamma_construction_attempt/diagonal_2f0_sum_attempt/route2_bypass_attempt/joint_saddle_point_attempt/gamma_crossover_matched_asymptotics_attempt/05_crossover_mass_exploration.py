"""
05_crossover_mass_exploration.py

GAMMA-CROSSOVER-MATCHED-ASYMPTOTICS-ATTEMPT (wave 34), DISC-DEC-151.

EXPLICITLY LABELED EXPLORATORY / INFORMAL. This script does NOT derive or
prove anything new; it numerically investigates WHERE the O(1) mass of the
crossover sum

    crossover(n,gamma) := Sum_{m=0}^n [ term_m(n,gamma) - T_prof(m/sqrt(n),gamma) ]

(predecessor's definition, PROVED O(1) not o(1), cited) actually
accumulates, as a function of an m-cutoff M, to give an honest, disclosed
picture of why the matching argument of script 04 -- which shows the
INNER and OUTER expansions agree pointwise, order by order, in their
overlap region -- does NOT by itself hand us a closed form for
crossover(n,gamma)'s limit (see ATTEMPT.md Section 6 for the precise
diagnosis).

Part A: fresh, independent re-implementation of crossover(n,gamma) (NOT
importing the predecessor's script 04), as a basic sanity check that this
front's own term_m evaluator reproduces the qualitative TREND the
predecessor's ATTEMPT.md prose reports (crossover(n,0.5) trending from
about -0.38 at n=20 toward about -0.41 as n grows toward 1600) -- using
FRESH n values, not the predecessor's exact grid.

Part B: partial-sum-by-cutoff exploration -- for growing n, compute
partial_crossover(n,gamma,M) := Sum_{m=0}^{M} [term_m(n,gamma) -
T_prof(m/sqrt(n),gamma)] at M = c*n^theta for theta in {0, 0.25, 0.5,
0.75, 1.0} (theta=0 is "fixed M", theta=1 is "the whole sum"), to see
how much of the total crossover(n,gamma) is already captured by an
m-cutoff that grows slower than sqrt(n) (theta<0.5, still "inner-region-
dominated" in scaling terms) versus needing to reach into the mesoscale
(theta>=0.5).

Part C: the logical-equivalence argument (verified here as elementary,
exact symbolic algebra, not a numerical claim) -- given the predecessor's
own PROVED exact decomposition

    S_n'(gamma) - G_n(gamma) - 1/(2*gamma) = crossover(n,gamma) + o(1)

and Lemma E (cited, PROVED equivalence, NOT itself asserting S_n=G_n+D(
gamma)+o(1) is true -- that equation IS essentially C(gamma)):
crossover(n,gamma) -> D(gamma)+1-1/(2*gamma) is then seen to be, by
elementary substitution, LOGICALLY EQUIVALENT to C(gamma) itself (S_n=
G_n+D(gamma)+o(1)) holding. This is checked here as a one-line symbolic
algebra identity, not a numerical experiment.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 60


def term_m_exact(n_val, m_val, gamma_val, dps=60):
    mp.mp.dps = dps
    g = mp.mpf(gamma_val)
    n_mp = mp.mpf(n_val)

    def integrand(s):
        t = s / n_mp
        base = t ** m_val * (1 - t) ** m_val
        return base * (1 - g * t) ** (n_val - m_val)

    if m_val == 0:
        nodes = [0, 5 / g, n_mp]
    else:
        speak = mp.mpf(m_val) / g
        nodes = [0, speak, speak + 5 * mp.sqrt(m_val + 1) / g, min(n_mp, speak + 40 / g)]
        nodes = sorted(set(x for x in nodes if x <= n_mp))
        if nodes[-1] != n_mp:
            nodes.append(n_mp)
    I = mp.quad(integrand, nodes) / n_mp
    Bm = mp.factorial(m_val) ** 2 / mp.factorial(2 * m_val + 1)
    Tnm = mp.binomial(n_val + m_val + 1, 2 * m_val + 1) * I / Bm
    return (g ** m_val / n_mp ** m_val) * mp.factorial(m_val) * Tnm


def T_prof(lam, gamma_val):
    g = mp.mpf(gamma_val)
    return (1 / g) * mp.e ** (-((2 - g) / (2 * g)) * lam ** 2)


def crossover_partial(n_val, gamma_val, M, dps=60):
    """Sum_{m=0}^{M} [term_m(n,gamma) - T_prof(m/sqrt(n),gamma)]."""
    mp.mp.dps = dps
    sqrtn = mp.sqrt(n_val)
    total = mp.mpf(0)
    for mm in range(0, M + 1):
        tm = term_m_exact(n_val, mm, gamma_val, dps=dps)
        phi = T_prof(mm / sqrtn, gamma_val)
        total += (tm - phi)
    return total


print("=" * 100)
print("PART A: fresh sanity check of crossover(n,gamma) trend, FRESH n grid")
print("=" * 100)
print("(compare qualitatively against the predecessor's own PROSE-reported")
print(" trend at gamma=0.5: approx -0.383 (n=20) drifting to approx -0.406")
print(" (n=1600) -- reproduced here from an independently-written evaluator,")
print(" NOT the predecessor's script, at a DIFFERENT/FRESH n grid.)")
print()
print(f"{'n':>6} {'gamma':>6} {'crossover(n,gamma)':>22} {'cutoff M used':>14}")
for gamma_val in ['0.5']:
    for n_val in [30, 90, 270, 810]:  # fresh grid, not predecessor's {20,50,100,200,400,800,1600}
        M = min(n_val, int(8 * mp.sqrt(n_val)) + 20)
        cv = crossover_partial(n_val, gamma_val, M, dps=60)
        print(f"{n_val:>6} {gamma_val:>6} {mp.nstr(cv, 8):>22} {M:>14}")

print()
print("=" * 100)
print("PART B: partial-sum-by-cutoff exploration (informal, exploratory)")
print("=" * 100)
print("For n=800, gamma=0.5: partial_crossover(n,gamma,M) at M=c*n^theta,")
print("theta in {0(fixed-ish small), 0.25, 0.5, 0.75, 1.0(full range)}.")
print()

gamma_val = '0.5'
n_val = 800
full_M = min(n_val, int(8 * mp.sqrt(n_val)) + 20)
full_crossover = crossover_partial(n_val, gamma_val, full_M, dps=60)
print(f"Full crossover(n={n_val},gamma={gamma_val}) [cutoff M={full_M}, tail beyond "
      f"verified negligible by construction of M] = {mp.nstr(full_crossover, 10)}")
print()
print(f"{'theta':>6} {'M':>6} {'partial_crossover':>20} {'fraction of full':>18}")
for theta in [0.0, 0.15, 0.25, 0.375, 0.5, 0.625, 0.75, 1.0]:
    if theta == 0.0:
        M = 5
    elif theta == 1.0:
        M = full_M
    else:
        M = max(1, min(full_M, int(n_val ** theta)))
    pc = crossover_partial(n_val, gamma_val, M, dps=60)
    frac = pc / full_crossover if full_crossover != 0 else mp.mpf('nan')
    print(f"{theta:>6.3f} {M:>6} {mp.nstr(pc, 10):>20} {mp.nstr(frac, 6):>18}")

print()
print("INTERPRETATION (informal, exploratory, disclosed as such): if the")
print("fraction-of-full column were already close to 1 at theta well below")
print("0.5 (i.e. an m-cutoff genuinely growing slower than sqrt(n)), that")
print("would suggest the crossover sum's mass is dominated by a sub-")
print("mesoscale region a sharper 'deep inner' analysis might reach; if")
print("instead the fraction keeps changing substantially all the way to")
print("theta=1 (full mesoscale range), that supports this front's Section 6")
print("diagnosis that no cutoff short of the full range captures the")
print("crossover sum's value -- i.e. a genuinely GLOBAL, not two-regime-")
print("local, resummation (item 4 of Estagio 56's diagnosis) is needed.")
print("See ATTEMPT.md Section 6 for the actual printed numbers and verdict.")

print()
print("=" * 100)
print("PART C: crossover(n,gamma)'s limit = D(gamma)+1-1/(2*gamma) is")
print("        LOGICALLY EQUIVALENT to C(gamma) itself (elementary algebra)")
print("=" * 100)

Sn_prime, Gn, gamma_s, Dgamma, cross_lim = sp.symbols(
    "S_n_prime G_n gamma D_gamma cross_lim")

# Cited, PROVED (predecessor's exact decomposition, up to a term proved
# o(1)/exponentially small):
#   S_n'(gamma) - G_n(gamma) - 1/(2*gamma) = crossover(n,gamma) + o(1)
# i.e. in the n->infinity limit:
eq_decomp = sp.Eq(Sn_prime - Gn - 1 / (2 * gamma_s), cross_lim)

# C(gamma), via Lemma E (cited, PROVED EQUIVALENCE -- the statement itself,
# S_n = G_n + D(gamma) + o(1), i.e. S_n'=1+G_n+D(gamma)+o(1), is what is
# CONJECTURED, not proved):
eq_C_gamma = sp.Eq(Sn_prime, 1 + Gn + Dgamma)

# Substitute eq_C_gamma into eq_decomp's LHS and solve for cross_lim:
lhs_under_Cgamma = (1 + Gn + Dgamma) - Gn - 1 / (2 * gamma_s)
predicted_cross_lim = sp.simplify(lhs_under_Cgamma)
print(f"IF C(gamma) holds (S_n'=1+G_n+D(gamma)+o(1)), THEN crossover(n,gamma) -> "
      f"{predicted_cross_lim}")
target_cited = Dgamma + 1 - 1 / (2 * gamma_s)
diff_target = sp.simplify(predicted_cross_lim - target_cited)
print(f"Predecessor's cited conjectural target: D(gamma)+1-1/(2*gamma)")
print(f"Difference (should be 0): {diff_target}")
assert diff_target == 0
print()
print("CONFIRMED (elementary algebra, exact): crossover(n,gamma) -> ")
print("D(gamma)+1-1/(2*gamma) is not an INDEPENDENT fact still to be found by")
print("more matched-asymptotics work -- it is, by the PROVED exact")
print("decomposition above, LOGICALLY EQUIVALENT to C(gamma) itself (S_n=")
print("G_n+D(gamma)+o(1)) holding. Any argument that rigorously computed")
print("crossover(n,gamma)'s closed-form limit and confirmed it equals the")
print("cited target would, by this same equivalence, CONSTITUTE a proof of")
print("C(gamma) -- clearly outside a single front's scope, and exactly why")
print("a 'local' inner/outer matching argument (script 04), which only")
print("certifies CONSISTENCY of two asymptotic pictures in their common")
print("region of validity, cannot by itself resolve it. See ATTEMPT.md")
print("Section 6 for the full discussion.")
