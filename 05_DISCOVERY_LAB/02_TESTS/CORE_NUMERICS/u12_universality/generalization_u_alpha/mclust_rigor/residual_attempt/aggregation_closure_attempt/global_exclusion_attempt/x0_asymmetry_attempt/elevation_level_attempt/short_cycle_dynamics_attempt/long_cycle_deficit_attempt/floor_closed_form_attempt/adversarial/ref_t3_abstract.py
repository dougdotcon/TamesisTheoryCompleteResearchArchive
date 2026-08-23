"""
ref_t3_abstract.py -- referee's own independent simulator of the "abstract
recursive gap re-entry process" described in ATTEMPT.md Sec 3.1/Sec 4 (T3),
built from that prose description alone. fcd_t3.py and abstract_sim.py were
NOT read or imported.

Process, as specified in the target document and restated in the mandate:
  State (s, g): s = total mass explored (fraction of n), g = remaining gap
  to x0 (fraction of n). Mode in {G, E}.
    - Mode G: "actively sweeping the gap": s and g move together at unit
      "speed" (ds=-dg) until either (a) g hits 0 first -> SUCCESS
      (boundary condition Phi(s,0)=1), or (b) a "mark" (rate c per unit s
      consumed) occurs first, interrupting the sweep at the new (s,g).
    - Mode E: "generic exploration": s increases at unit speed, g fixed,
      until a mark occurs (rate c per unit s consumed).
  At a mark (whichever mode), resolve using the CURRENT (s,g) at that
  instant:
    - w.p. s: KILL (absorbed into an already-explored point -> permanent
      FAILURE, contributes 0)
    - w.p. g: LAND IN GAP -- new gap g' ~ Uniform(0, g) (uniform re-entry
      point within the old gap), mode -> G, s unchanged at the instant
    - w.p. 1-s-g: GENERIC -- mode -> E, g unchanged, s unchanged at the
      instant (accrues afterward at unit speed same as always)
  This matches Sec 5's PDEs (kill contributes 0 to W, hence absent from the
  W(s,g) formula; W = g*Avg_g[Phi(s,.)] + (1-s-g)*Psi(s,g)) and Sec 3.1's
  "kill w.p. s, land in gap w.p. g else generic (mode E, g unchanged, s
  accrues)" prose exactly.

Implemented as an EXACT (no time-discretization) continuous-time / event-
driven simulation, fully vectorized across a population of N instances
per t0 (marks occur at independent Exp(c) increments of s; the process is
simulated exactly at each event, not approximated on a grid).

Target: phi_abstract(t0) := P(success | start at s=0, g=t0, mode=G), for
the SAME t0 grid as the front's own T3 table, so results are directly
comparable; N=200000 per t0 (5x the front's own N=40000).

Seed: SeedSequence(20260834004), referee-reserved range (DISC-DEC-057),
confirmed unused elsewhere before use.
"""
import time
import numpy as np


def simulate_abstract(t0, c, N, rng, max_iters=20000):
    s = np.zeros(N)
    g = np.full(N, float(t0))
    is_G = np.ones(N, dtype=bool)
    alive = np.ones(N, dtype=bool)
    outcome = np.zeros(N)

    it = 0
    while alive.any() and it < max_iters:
        it += 1
        idx = np.where(alive)[0]
        m = idx.size
        delta = rng.exponential(1.0 / c, size=m)

        cur_is_G = is_G[idx]
        cur_s = s[idx]
        cur_g = g[idx]

        # success this round only possible in mode G: delta >= g (reach x0 before next mark)
        succ_mask = cur_is_G & (delta >= cur_g)
        mark_mask = ~succ_mask

        new_s = cur_s.copy()
        new_g = cur_g.copy()

        g_mark = cur_is_G & mark_mask
        new_s[g_mark] = cur_s[g_mark] + delta[g_mark]
        new_g[g_mark] = cur_g[g_mark] - delta[g_mark]

        e_mark = (~cur_is_G) & mark_mask  # all E-mode active are "mark" (no success branch in E)
        new_s[e_mark] = cur_s[e_mark] + delta[e_mark]
        # clip to keep within simplex s+g<=1 (E mode can, in principle, overshoot with a
        # single large draw; G-mode conserves s+g exactly so never needs clipping)
        overshoot = e_mark & (new_s + new_g > 1.0)
        new_s[overshoot] = 1.0 - new_g[overshoot]

        # commit success
        success_idx = idx[succ_mask]
        outcome[success_idx] = 1.0
        alive[success_idx] = False

        # commit marked instances' state, then resolve the mark trichotomy
        marked_idx = idx[mark_mask]
        s[marked_idx] = new_s[mark_mask]
        g[marked_idx] = new_g[mark_mask]

        cs = s[marked_idx]
        cg = g[marked_idx]
        u = rng.random(marked_idx.size)
        kill_mask = u < cs
        gap_mask = (~kill_mask) & (u < cs + cg)
        generic_mask = ~kill_mask & ~gap_mask

        kill_idx = marked_idx[kill_mask]
        alive[kill_idx] = False  # outcome stays 0

        gap_idx = marked_idx[gap_mask]
        gap_g_vals = cg[gap_mask]
        new_gap_vals = rng.random(gap_idx.size) * gap_g_vals
        g[gap_idx] = new_gap_vals
        is_G[gap_idx] = True

        generic_idx = marked_idx[generic_mask]
        is_G[generic_idx] = False
        # (s,g unchanged further for generic_idx at this instant; already committed above)

    n_unresolved = int(alive.sum())
    return outcome, n_unresolved, it


if __name__ == "__main__":
    c = 1000
    N = 200000  # 5x the front's own N=40000
    t0_list = [0.0001, 0.001, 0.01, 0.09, 0.37, 0.90]

    master = np.random.SeedSequence(20260834004)
    children = master.spawn(len(t0_list))

    print(f"ref_t3_abstract: c={c} N={N} per t0")
    print(f"{'t0':>8} {'phi_abstract':>14} {'SEM':>10} {'n_unresolved':>13} {'n_iters':>8}")
    results = []
    t_start = time.time()
    for t0, child in zip(t0_list, children):
        rng = np.random.default_rng(child)
        outcome, n_unres, n_iters = simulate_abstract(t0, c, N, rng)
        phi = outcome.mean()
        sem = outcome.std(ddof=1) / np.sqrt(N)
        print(f"{t0:>8.4f} {phi:>14.5f} {sem:>10.5f} {n_unres:>13d} {n_iters:>8d}")
        results.append((t0, phi, sem, n_unres))
    print(f"total time: {time.time()-t_start:.1f}s")

    phis = np.array([r[1] for r in results])
    # pre-reg-style plateau criterion (matching the front's own): ratio of phi at the
    # two largest t0 to the t0=0.09 value stays in [0.5, 2]x
    idx09 = t0_list.index(0.09)
    ref = phis[idx09]
    ratios = phis[-2:] / ref
    print(f"\nplateau check: phi(t0=0.09)={ref:.5f}; ratios at last two t0 to this: {ratios}")
    print(f"Criterion (both in [0.5,2]x): {'MET' if np.all((ratios>=0.5)&(ratios<=2.0)) else 'NOT MET'}")
