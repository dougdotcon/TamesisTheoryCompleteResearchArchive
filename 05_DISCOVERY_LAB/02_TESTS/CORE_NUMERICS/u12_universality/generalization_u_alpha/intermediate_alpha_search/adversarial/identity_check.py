"""
Adversarial Monte Carlo: attack the claimed identity H(t) = t*Lambda(t)/c
directly, i.e. P(x0 cyclic | T0=t) = exp(-t*Lambda(t)) for the M-WEIB(beta)
process, WITHOUT going through the full phi(c) integral over t.

Own construction (independent of the target report's code, not read):
Condition on T0 = t (x0's own closure clock). Marks in [0,t) of a
non-homogeneous Poisson process with mean-value function Lambda(s)=c*s^beta
restricted to [0,t) have count K_t ~ Poisson(Lambda(t)) and i.i.d.
positions with density lambda(s)/Lambda(t) = beta*s^(beta-1)/t^beta on
[0,t); by direct CDF inversion this is S = t * V^(1/beta), V~Unif(0,1).

Each mark independently "fails" (kills, i.e. destination lands on
already-visited mass [Theta < S]; or survives but its own sibling
arc-head closes before t [Theta >= S and T = S+(1-S)(1-e^-E) <= t]).
Success for x0 (given T0=t) requires ZERO failing marks in [0,t).

Claim under test: P(zero failing marks) = exp(-t*Lambda(t)) for EVERY t,
beta, c -- i.e. the per-mark failure probability, once we integrate out
its own random Theta,E pair, is exactly t regardless of the mark's
position s (the "bracket(s,t)=t" claim), and this survives an arbitrary
(non-constant) mark arrival intensity.
"""
import numpy as np
import json

def theoretical_H(t, c, beta):
    Lambda_t = c * t**beta
    return t * Lambda_t

def simulate_cell(t, c, beta, n_trials, rng):
    Lambda_t = c * (t ** beta)
    K = rng.poisson(Lambda_t, size=n_trials)
    max_K = K.max() if n_trials > 0 else 0
    if max_K == 0:
        n_fail = np.zeros(n_trials, dtype=bool)
        return float(np.mean(~n_fail)), 0, n_trials

    # Build a ragged batch via a flat array + trial index, vectorized.
    total_marks = int(K.sum())
    trial_idx = np.repeat(np.arange(n_trials), K)

    V = rng.uniform(0.0, 1.0, size=total_marks)
    S = t * (V ** (1.0 / beta))               # Beta(beta,1) on [0,t), scaled
    Theta = rng.uniform(0.0, 1.0, size=total_marks)
    E = rng.exponential(1.0, size=total_marks)

    kill = Theta < S
    Tclock = S + (1.0 - S) * (1.0 - np.exp(-E))
    survive_but_closes = (~kill) & (Tclock <= t)
    fails = kill | survive_but_closes

    any_fail_per_trial = np.zeros(n_trials, dtype=bool)
    np.logical_or.at(any_fail_per_trial, trial_idx, fails)

    p_success_hat = float(np.mean(~any_fail_per_trial))
    return p_success_hat, total_marks, n_trials

def main():
    rng = np.random.default_rng(20260823)  # pre-registered seed
    N_TRIALS = 300_000

    t_grid = [0.1, 0.3, 0.5, 0.7, 0.9]
    beta_grid = [0.25, 0.5, 0.75]
    c_grid = [1.0, 4.0, 16.0]

    rows = []
    n_within_3sigma = 0
    n_total = 0
    print(f"{'beta':>6} {'c':>6} {'t':>5} {'p_hat':>10} {'p_theory':>10} {'z':>7} {'within3s':>9}")
    for beta in beta_grid:
        for c in c_grid:
            for t in t_grid:
                p_hat, total_marks, n = simulate_cell(t, c, beta, N_TRIALS, rng)
                H = theoretical_H(t, c, beta)
                p_theory = np.exp(-H)
                se = np.sqrt(max(p_theory * (1 - p_theory), 1e-12) / n)
                z = (p_hat - p_theory) / se if se > 0 else 0.0
                within = bool(abs(z) < 3.0)
                n_total += 1
                n_within_3sigma += int(within)
                rows.append(dict(beta=beta, c=c, t=t, p_hat=p_hat, p_theory=float(p_theory),
                                  se=float(se), z=float(z), within_3sigma=within,
                                  mean_marks_in_0t=total_marks / n))
                print(f"{beta:6.2f} {c:6.1f} {t:5.2f} {p_hat:10.6f} {p_theory:10.6f} {z:7.2f} {str(within):>9}")

    frac_pass = n_within_3sigma / n_total
    summary = dict(n_cells=n_total, n_within_3sigma=n_within_3sigma, frac_pass=frac_pass,
                    n_trials_per_cell=N_TRIALS, seed=20260823, rows=rows)
    with open("identity_check_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\n{n_within_3sigma}/{n_total} cells within 3 sigma ({frac_pass:.1%})")
    print("Saved identity_check_results.json")

if __name__ == "__main__":
    main()
