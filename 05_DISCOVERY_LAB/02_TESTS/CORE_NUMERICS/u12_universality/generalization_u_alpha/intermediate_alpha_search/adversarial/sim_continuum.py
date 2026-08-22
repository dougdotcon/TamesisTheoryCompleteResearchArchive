"""
Adversarial Simulator A (continuum, own construction, not based on any
code read from the target front): direct Monte Carlo of the FULL M-WEIB
model (unconditional on T0), to validate phi_WEIB(c;beta) =
integral_0^1 exp(-c t^(1+beta)) dt and the tail exponent alpha=1/(1+beta).

Construction (own route, independent of Definition 3's algorithm as
literally written -- this samples the whole mark process directly
instead of running an incremental loop):
  - T0 = 1 - exp(-E0), E0 ~ Exp(1)  (equivalently Unif(0,1), but we
    generate it via the same exponential-clock primitive as the base
    construction, to keep the closure-clock machinery uniform).
  - K ~ Poisson(c)  (total marks over [0,1); Lambda(1)=c since
    Lambda(t)=c*t^beta).
  - S_1..S_K iid with density beta*s^(beta-1) on (0,1) i.e. Beta(beta,1)
    -> sampled as U^(1/beta), U~Unif(0,1).
  - Theta_1..Theta_K iid Unif(0,1) (destinations, M-U rule: kill iff
    Theta_j < S_j).
  - E_1..E_K iid Exp(1) -> closure clock of surviving arc-head j:
    T_j = S_j + (1-S_j)*(1-exp(-E_j)).
  - x0 cyclic iff: sort marks by S; walk through them in increasing S
    order maintaining running_min_T (starting at T0); a mark before the
    current running_min_T that kills -> not cyclic, stop. A mark before
    running_min_T that survives -> update running_min_T = min(running_min_T, T_j)
    (a new arc-head enters the race) and continue. A mark at or after
    running_min_T is never reached (exploration already stopped at
    running_min_T). If we exhaust all marks below running_min_T without
    a kill -> cyclic iff the eventual minimizer is T0, but by
    construction (only T0 starts the race and any T_j > running_min_T
    at the time it's created is irrelevant) x0 is cyclic iff no kill
    ever interrupts before we run out of marks with S_j < running_min_T.
    This is implemented directly (own code), fully vectorized per batch
    for speed, with an explicit per-trial Python loop only over the
    (small, Poisson(c)) number of marks -- unavoidable due to the
    sequential stopping rule, but batched across trials via numpy for
    the RNG draws.
"""
import numpy as np
import json
import time

def simulate_phi(c, beta, n_trials, rng):
    E0 = rng.exponential(1.0, size=n_trials)
    T0 = 1.0 - np.exp(-E0)

    K = rng.poisson(c, size=n_trials)
    total_marks = int(K.sum())
    if total_marks == 0:
        cyclic = np.ones(n_trials, dtype=bool)
        return float(np.mean(cyclic)), n_trials

    trial_idx = np.repeat(np.arange(n_trials), K)
    U = rng.uniform(0.0, 1.0, size=total_marks)
    S = U ** (1.0 / beta)
    Theta = rng.uniform(0.0, 1.0, size=total_marks)
    E = rng.exponential(1.0, size=total_marks)
    Tclock = S + (1.0 - S) * (1.0 - np.exp(-E))
    kill = Theta < S

    # Sort marks within each trial by S: sort globally by (trial_idx, S)
    order = np.lexsort((S, trial_idx))
    trial_idx_s = trial_idx[order]
    S_s = S[order]
    Tclock_s = Tclock[order]
    kill_s = kill[order]

    # Process each trial's marks in increasing S order with the running
    # min-closure-time stopping rule. Vectorized across trials is not
    # straightforward because the stopping point differs per trial;
    # implement with a compact per-trial loop using split indices
    # (fast enough: total_marks ~ n_trials*c, split via searchsorted).
    counts = K
    offsets = np.zeros(n_trials + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(counts)

    cyclic = np.empty(n_trials, dtype=bool)
    for i in range(n_trials):
        lo, hi = offsets[i], offsets[i + 1]
        running_min_T = T0[i]
        winner_is_x0 = True   # BUGFIX (found by adversary): must track WHO
        # currently holds the running minimum closure time, not merely
        # whether a kill has occurred. Definition 3 requires i*=0 (x0 is
        # the minimizer among ALL arc-heads, incl. T0), not just "no kill
        # ever fires". A first, buggy version of this script set
        # is_cyclic=True whenever no kill occurred, which silently ignores
        # the case where some OTHER surviving arc-head's closure time Tj
        # undercuts T0 (Tj < running_min_T) without ever triggering a kill
        # -- that must count as x0 NOT cyclic (i* != 0), even absent any
        # kill. Caught by comparing against the independently-validated
        # identity_check.py construction (T0-conditional restriction to
        # [0,t)), which disagreed sharply with this script's first version
        # (phi_hat >> phi_theory in every single cell, by >100 sigma) --
        # see ADVERSARIAL_VERDICT.md for the full account.
        is_cyclic = True
        for j in range(lo, hi):
            s = S_s[j]
            if s >= running_min_T:
                break  # exploration already stopped before reaching this mark
            if kill_s[j]:
                is_cyclic = False
                break
            tj = Tclock_s[j]
            if tj < running_min_T:
                running_min_T = tj
                winner_is_x0 = False
        cyclic[i] = is_cyclic and winner_is_x0

    return float(np.mean(cyclic)), n_trials

def closed_form_quad(c, beta, n=4000):
    t = np.linspace(0, 1, n + 1)
    y = np.exp(-c * t ** (1 + beta))
    return np.trapezoid(y, t)

def main():
    rng = np.random.default_rng(20260822)  # pre-registered seed
    N_TRIALS = 300_000

    beta_grid = [0.25, 0.5, 0.75, 0.9]  # 0.9 is the extra value not in their tested grid
    c_grid = [0.5, 1, 2, 4, 8, 16, 32, 64]

    rows = []
    t0 = time.time()
    print(f"{'beta':>6} {'c':>6} {'phi_hat':>10} {'phi_theory':>10} {'z':>7} {'se':>9}")
    for beta in beta_grid:
        for c in c_grid:
            phi_hat, n = simulate_phi(c, beta, N_TRIALS, rng)
            phi_theory = closed_form_quad(c, beta)
            se = np.sqrt(max(phi_theory * (1 - phi_theory), 1e-12) / n)
            z = (phi_hat - phi_theory) / se if se > 0 else 0.0
            rows.append(dict(beta=beta, c=c, phi_hat=phi_hat, phi_theory=float(phi_theory),
                              se=float(se), z=float(z), n_trials=n))
            print(f"{beta:6.2f} {c:6.1f} {phi_hat:10.6f} {phi_theory:10.6f} {z:7.2f} {se:9.6f}")
        print(f"  [elapsed {time.time()-t0:.1f}s]")

    with open("sim_continuum_results.json", "w") as f:
        json.dump(dict(seed=20260822, n_trials_per_cell=N_TRIALS, rows=rows), f, indent=2)
    print(f"\nTotal time: {time.time()-t0:.1f}s")
    print("Saved sim_continuum_results.json")

if __name__ == "__main__":
    main()
