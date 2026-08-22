"""
Adversarial Simulator B (finite-n, own construction, not based on any
code read from the target front): "lazy revelation" walk of x0's own
forward orbit under a finite-n M-WEIB(beta) mapping.

Design note (worked out BEFORE coding, see ADVERSARIAL_NOTE.md): marking
by FIXED EXTERNAL LABEL (as in the standard M_n(c) baseline, Definition 1
of THEOREM.md) would NOT create a genuinely time-varying rate along the
orbit -- since pi is uniform random, the walk visits an effectively
uniform-random subset of labels regardless of position, so a fixed
label-based marking probability p_i=f(i/n) averages out to an effectively
CONSTANT rate in the continuum limit, not the intended non-homogeneous
one. Instead, the marking (reroute) decision must be tied to the RANK OF
VISITATION along x0's own walk (step k -> mass ~k/n), which is exactly
what "t = fraction of orbit mass traversed" means operationally. This is
implemented by lazily revealing pi one step at a time as the walk
proceeds, deciding at each step whether it is a reroute (uniform
destination in [n], unconstrained) or a genuine pi-step (uniform among
labels not yet used as a pi-image, but with x0 itself always eligible as
a target, since normal pi-closure onto x0 is exactly how an unperturbed
cycle closes).

Bin-probability correction (found and fixed BEFORE running, documented
honestly): using the naive per-step probability Lambda((k+1)/n)-Lambda(k/n)
directly as a Bernoulli probability breaks down when beta<1 and c is
large, since the intensity is singular at t=0 (density ~ c*beta*t^(beta-1))
and the mean number of events in the first bin can exceed 1 (e.g. c=64,
beta=0.25, n=2000 gives an expected ~9.6 events in the first slot alone).
The correct, standard NHPP-to-discrete-slot construction uses
P(>=1 event in bin) = 1 - exp(-(Lambda(t_hi)-Lambda(t_lo))), which stays
in [0,1] for any bin mass and reduces to the naive linear approximation
when the bin mass is small (the well-behaved regime) -- used throughout.
"""
import numpy as np
import json
import time

def simulate_trial_batch(n, c, beta, n_trials, rng, max_steps=None):
    if max_steps is None:
        max_steps = n  # hard cap; walk cannot exceed n steps
    results = np.empty(n_trials, dtype=bool)
    steps_taken = np.empty(n_trials, dtype=np.int64)

    for tr in range(n_trials):
        path_set = {0}
        # BUGFIX (found by adversary, before the full grid was accepted):
        # a first version excluded ALL previously-visited labels (path_set)
        # from the follow-pi sampling pool. That is wrong: pi is an
        # independent bijection from the reroute stream, so only labels
        # already revealed as a PI-IMAGE (via an earlier follow-pi step)
        # should be excluded -- a label visited only via an earlier REROUTE
        # remains a perfectly legitimate (and, if hit, collision-causing)
        # target for pi. Excluding the whole path artificially protected
        # every trial from ever colliding with its own reroute-visited
        # points via the pi channel, systematically inflating phi_hat (a
        # bias that, tellingly, did NOT shrink with n -- the tell that it
        # was a construction bug, not a genuine finite-n effect). Caught by
        # noticing phi_hat - phi_continuum stayed a large, roughly
        # n-independent constant across n=2000/8000/32768, inconsistent
        # with a real O(1/n)-type finite-size correction.
        pi_used_targets = set()
        k = 0
        cyclic = False
        while k < max_steps:
            t_lo = k / n
            t_hi = (k + 1) / n
            dLambda = c * (t_hi ** beta - t_lo ** beta) if t_lo > 0 else c * (t_hi ** beta)
            p_reroute = 1.0 - np.exp(-dLambda) if dLambda > 0 else 0.0
            is_reroute = rng.random() < p_reroute
            if is_reroute:
                target = int(rng.integers(0, n))
            else:
                # rejection-sample a target not already used as a PI-image
                # (label 0 is always eligible: normal pi-closure onto x0)
                while True:
                    cand = int(rng.integers(0, n))
                    if cand == 0 or cand not in pi_used_targets:
                        target = cand
                        break
            if target == 0:
                cyclic = True
                break
            if target in path_set:
                cyclic = False
                break
            path_set.add(target)
            if not is_reroute:
                pi_used_targets.add(target)
            k += 1
        results[tr] = cyclic
        steps_taken[tr] = k
    return results, steps_taken

def closed_form_quad(c, beta, npts=4000):
    t = np.linspace(0, 1, npts + 1)
    y = np.exp(-c * t ** (1 + beta))
    return np.trapezoid(y, t)

def main():
    rng = np.random.default_rng(20260824)  # pre-registered seed

    beta_grid = [0.25, 0.5, 0.75]
    c_grid = [1.0, 4.0, 16.0]
    # NOTE: revised down from the pre-registered 20000/20000/4000 after
    # timing showed mean walk length is O(n) (a sizeable fraction of the
    # full mass, not O(sqrt n) as guessed when the note was written --
    # permutation cycle lengths are order n, unlike random-mapping "rho"
    # shapes) making the original counts too slow for the time budget.
    # Trial counts rescaled roughly as 1/n to keep per-cell wall time
    # comparable; this is a budget adjustment only, not a change to the
    # grid of (n, beta, c) values themselves, which stays as pre-registered.
    n_trials_map = {2000: 4000, 8000: 1500, 32768: 400}

    rows = []
    t_start = time.time()
    for n, n_trials in n_trials_map.items():
        for beta in beta_grid:
            for c in c_grid:
                t0 = time.time()
                res, steps = simulate_trial_batch(n, c, beta, n_trials, rng)
                phi_hat = float(res.mean())
                phi_cont = closed_form_quad(c, beta)
                se = np.sqrt(max(phi_hat * (1 - phi_hat), 1e-12) / n_trials)
                dt = time.time() - t0
                mean_steps = float(steps.mean())
                rows.append(dict(n=n, beta=beta, c=c, phi_hat=phi_hat,
                                  phi_continuum=float(phi_cont),
                                  diff_from_continuum=phi_hat - phi_cont,
                                  se=float(se), n_trials=n_trials,
                                  mean_steps=mean_steps, elapsed_s=dt))
                print(f"n={n:6d} beta={beta:.2f} c={c:5.1f}  phi_hat={phi_hat:.5f}  "
                      f"phi_cont={phi_cont:.5f}  diff={phi_hat-phi_cont:+.5f}  "
                      f"se={se:.5f}  mean_steps={mean_steps:.1f}  [{dt:.1f}s]")
    total = time.time() - t_start
    print(f"\nTotal time: {total:.1f}s")

    with open("sim_finiten_results.json", "w") as f:
        json.dump(dict(seed=20260824, n_trials_map=n_trials_map, rows=rows), f, indent=2)
    print("Saved sim_finiten_results.json")

if __name__ == "__main__":
    main()
