#!/usr/bin/env python3
"""
REFEREE script 03 -- robustness check of the front's Sec 4 Part C "bonus
observation" (the 1/sqrt(2) convergence-ratio pattern for the crossover
sum's distance from the conjectural D(gamma)+1-1/(2*gamma) target).

Independent implementation (primary double-sum T(n,m), no front code read),
at gamma values DISJOINT from the front's own (0.3,0.5,0.8) AND from this
referee's own script 02 grid (0.25,0.6,0.9): gamma in {0.35, 0.7}.

n grid matches the front's own doubling structure (100,200,400,800,1600) so
the SAME doubling-ratio comparison can be made -- the point of this check is
whether the 1/sqrt(2) pattern the front reports is a genuine feature at
OTHER gamma, or an artifact of the specific 3 gamma values the front tested.
"""
import mpmath as mp
import time

mp.mp.dps = 50

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def T_nm_direct(n, m, gamma):
    total = mp.mpf(0)
    for j in range(0, n - m + 1):
        total += mp.binomial(j + m, m) * mp.binomial(n - j, m) * (1 - gamma) ** j
    return total


def term_m(n, m, gamma):
    T = T_nm_direct(n, m, gamma)
    return (gamma ** m / mp.mpf(n) ** m) * mp.factorial(m) * T


def T_prof(lam, gamma):
    return (1 / gamma) * mp.e ** (-((2 - gamma) / (2 * gamma)) * lam ** 2)


def G_n(n, gamma):
    beta = gamma * (2 - gamma) / 2
    return mp.sqrt(n) * mp.mpf('0.5') * mp.sqrt(mp.pi / beta)


def D0_proved(gamma):
    return (gamma - 1) / (2 * (2 - gamma))


def E_heuristic_conjectured(gamma):
    return (-3 * gamma ** 2 + 7 * gamma - 6) / (6 * (gamma - 2) ** 2)


gammas = [mp.mpf('0.35'), mp.mpf('0.7')]
n_values = [100, 200, 400, 800, 1600]

log("=" * 78)
log("Independent reproduction of the crossover-sum-vs-conjectural-target")
log("1/sqrt(2) doubling-ratio check, at FRESH gamma values (0.35, 0.7),")
log("disjoint from both the front's own grid (0.3,0.5,0.8) and this referee's")
log("own script 02 grid (0.25,0.6,0.9). Primary double-sum T(n,m), no")
log("quadrature, no front code read.")
log("=" * 78)

all_crossover = {}
t_start = time.time()
for gamma in gammas:
    log(f"\n--- gamma = {float(gamma)} ---")
    rows = []
    for n in n_values:
        t0 = time.time()
        M = min(n, int(8 * mp.sqrt(n)) + 20)
        crossover = mp.mpf(0)
        for m in range(0, M + 1):
            tm = term_m(n, m, gamma)
            tp = T_prof(mp.mpf(m) / mp.sqrt(n), gamma)
            crossover += (tm - tp)
        dt = time.time() - t0
        log(f"  n={n:>5} (M={M:>4}): crossover = {float(crossover):.10f}  [{dt:.1f}s]")
        rows.append((n, crossover))
    all_crossover[float(gamma)] = rows
log(f"\nTotal wall time: {time.time()-t_start:.1f}s")

log("")
log("=" * 78)
log("Doubling-ratio analysis vs the conjectural target D(gamma)+1-1/(2*gamma)")
log("=" * 78)
for gamma in gammas:
    D0 = D0_proved(gamma)
    Eh = E_heuristic_conjectured(gamma)
    target_residual = (D0 + Eh + 1) - 1 / (2 * gamma)
    rows = all_crossover[float(gamma)]
    log(f"\ngamma={float(gamma)}: target_residual (conjectural) = {float(target_residual):.10f}")
    diffs = []
    for n, crossover in rows:
        diff = abs(crossover - target_residual)
        diffs.append((n, diff))
        log(f"  n={n:>5}: |crossover-target| = {float(diff):.10f}")
    log("  doubling ratios (100->200->400->800->1600):")
    for i in range(1, len(diffs)):
        n_prev, d_prev = diffs[i - 1]
        n_cur, d_cur = diffs[i]
        ratio = d_cur / d_prev
        flag = "  <-- CLOSE TO 1/SQRT2" if abs(float(ratio) - 0.7071) < 0.02 else "  <-- DEPARTS"
        log(f"    n={n_prev}->{n_cur}: ratio = {float(ratio):.5f}  (1/sqrt2={float(1/mp.sqrt(2)):.5f}){flag}")

log("")
log("=" * 78)
log("CROSS-CHECK: re-examine the front's OWN reported ratios (from its own")
log("04_exact_decomposition_test.log, transcribed here for direct comparison,")
log("not recomputed) against its OWN prose claim in ATTEMPT.md Sec 4 Part C:")
log("'the ratio at successive doublings sitting at 0.708-0.713 ... for THREE")
log("consecutive doublings (100->200->400->800) at all three gamma tested'")
log("=" * 78)
front_ratios = {
    0.3: [0.70849, 0.70805, 0.70775, 0.59313],
    0.5: [0.71024, 0.70928, 0.69138, 0.33940],
    0.8: [0.71303, 0.71017, 0.56929, 0.42275],
}
log(f"{'gamma':>6} {'100->200':>10} {'200->400':>10} {'400->800':>10} {'800->1600':>10}")
for g, rs in front_ratios.items():
    log(f"{g:>6} {rs[0]:>10.5f} {rs[1]:>10.5f} {rs[2]:>10.5f} {rs[3]:>10.5f}")
all_three_doubling_ratios = [r for rs in front_ratios.values() for r in rs[:3]]
log(f"\nMin/max of the FIRST THREE doubling ratios (100->200,200->400,400->800),")
log(f"across all three gamma the front itself tested:")
log(f"  min = {min(all_three_doubling_ratios):.5f}, max = {max(all_three_doubling_ratios):.5f}")
log(f"  Front's claimed range: 0.708-0.713.")
log(f"  ACTUAL range spanned by the front's own printed data (transcribed")
log(f"  directly from 04_exact_decomposition_test.log, not altered): "
    f"{min(all_three_doubling_ratios):.5f}-{max(all_three_doubling_ratios):.5f}")
if min(all_three_doubling_ratios) < 0.70 or max(all_three_doubling_ratios) > 0.72:
    log("  ==> The front's OWN claimed range (0.708-0.713) does NOT bound its OWN")
    log("      printed data for all 'three consecutive doublings': at gamma=0.5 the")
    log("      400->800 ratio is 0.69138 (below the claimed 0.708 floor), and at")
    log("      gamma=0.8 the 400->800 ratio is 0.56929 -- essentially already in the")
    log("      'departure' regime the front's text reserves for the FINAL doubling")
    log("      only (800->1600). This is a genuine, independently-verifiable")
    log("      overclaim in the document's own characterization of its own data,")
    log("      not a recomputation discrepancy (the transcribed numbers ARE the")
    log("      front's own script 04 log output).")

with open("ref_03_bonus_observation_robustness.log", "w") as f:
    f.write("\n".join(LOG) + "\n")
print("\nDone.")
