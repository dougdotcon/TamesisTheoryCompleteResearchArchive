"""
Synthetic validation of `soc_common.py`, run and committed BEFORE any real
PRE/POST segment (Ridgecrest 2019, GOES solar flares) is touched -- required
by METHODOLOGY_NOTE.md validation discipline (same standard as
`critical_slowing_down`, `wavelet_multiresolution`, `dfa_multiscale_entropy`
in this lab).

Generative model for the positive/transition controls (documented choice,
see also `generate_branching_events` docstring in soc_common.py): an
immigration-birth branching process -- the classical Hawkes-process cluster
representation (Hawkes 1974, "Point spectra of some mutually exciting point
processes"; Hawkes & Oakes 1974, "A cluster process representation of a
self-exciting process") -- where every event (immigrant or offspring) spawns
Poisson(branching_ratio) direct offspring with i.i.d. Exponential(mean_delay)
time lags. Each immigrant's full descendant tree is EXACTLY a Galton-Watson
branching process with Poisson(branching_ratio) offspring, so the marginal
distribution of total cluster size (immigrant + all descendants) is EXACTLY
the classical total-progeny distribution of a GW process:
  - at branching_ratio=1 (critical): the Borel(1) distribution, with
    P(size=n) = e^{-n} n^{n-1}/n!, which by Stirling's approximation is
    asymptotically P(size=n) ~ (2*pi)^{-1/2} * n^{-3/2} -- i.e. EXACTLY the
    theoretical tau=1.5 SOC/branching-process benchmark this candidate is
    built around (Otter 1949, "The multiplicative process"; Dwass 1969, "The
    total progeny in a branching process and a related random walk").
  - at branching_ratio<1 (subcritical): mean total progeny = 1/(1-m) is
    FINITE, and the tail decays faster than any power law (no clean
    power-law regime expected) -- used as the PRE (subcritical) synthetic
    segment in the transition control.
This was chosen over directly simulating a Galton-Watson tree in the
"generation" domain (no explicit event TIMES) specifically so the exact same
lambda/binning/avalanche-extraction machinery this module runs on Ridgecrest/
GOES timestamps is exercised end-to-end here too, not bypassed.

Five required checks (see task spec / METHODOLOGY_NOTE.md validation
section, including the "Adendo ao Gap (c)" addendum added after the first
four were run):
  1. POSITIVE CONTROL: standalone critical branching-process event stream
     (branching_ratio=1.0) -> confirm recovered tau close to the theoretical
     1.5.
  2. NEGATIVE CONTROL: standalone pure homogeneous Poisson event stream (no
     clustering) -> confirm the recovered tau does NOT land near 1.5 (i.e.
     the MLE/KS machinery does not spuriously "find" a power law where there
     is none).
  3. TRANSITION CONTROL (rate-matched): PRE = subcritical branching process
     (branching_ratio~0.5), POST = critical branching process
     (branching_ratio~1.0, tau~1.5) -> confirm Delta_tau/Delta_sigma from the
     real data fall outside (or are flagged by) the Poisson-surrogate null
     AND the paired-bootstrap-tau null.
  4. NEGATIVE CONTROL FOR THE NULL TEST: PRE and POST both drawn
     INDEPENDENTLY from the SAME generative process (both critical) -> a
     structurally null case, confirm p is typically not significant under
     both the Poisson-surrogate test and the paired-bootstrap-tau test.
  5. TRANSITION CONTROL, RATE-MISMATCHED (added for the "Adendo ao Gap (c)"
     paired-bootstrap-tau validation): SAME branching_ratio difference as
     check 3 (PRE=0.5 subcritical, POST=1.0 critical) but WITHOUT tuning
     `mu_immigrants` to equalize PRE/POST total event rate (both use the
     SAME `mu_immigrants` as each other, unlike check 3) -- this is exactly
     the scenario class that produced the p_tau=0.285 false-negative under
     the Poisson-surrogate test alone documented in METHODOLOGY_NOTE.md
     (large real Delta_tau, but a huge PRE/POST rate mismatch inflates the
     combined Poisson-surrogate null's dispersion). Confirms
     `p_bootstrap_tau` (the new PRIMARY test, immune to this rate-mismatch
     failure mode because each segment's bootstrap distribution is built
     purely from that segment's OWN observed avalanches) recovers power
     where `p_tau` does not.

PRE/POST event RATES are matched between conditions 3's PRE and POST as
closely as feasible (see `mu_immigrants` tuning below) specifically so a
genuine STRUCTURAL difference (subcritical vs critical) is being tested,
not primarily a RATE difference -- consistent with METHODOLOGY_NOTE.md gap
(a)'s explicit anti-rate-confound design intent for the shared `lambda`.
Check 5 deliberately removes this rate-matching to reproduce and validate
the fix for the power-loss failure mode documented in the Adendo.

Run: python3 validate_synthetic.py
Writes: validation_synthetic.json
"""
import json
import sys
import os
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from soc_common import (
    generate_branching_events, generate_homogeneous_poisson_events,
    compute_lambda, analyze_segment, run_soc_pipeline,
    N_SURROGATES, N_MLE_BOOTSTRAP, SEED,
)

# --------------------------------------------------------------------------
# Generative-model configuration (data-generation seeds -- distinct from and
# unrelated to the pipeline's own internal analysis SEED=12345 used for the
# Poisson-surrogate null and MLE bootstrap, which is applied unmodified
# inside run_soc_pipeline/analyze_segment as imported above).
# --------------------------------------------------------------------------
GEN_SEED_POS = 2024
GEN_SEED_NEG = 3033
GEN_SEED_TRANSITION = 555
GEN_SEED_NULL_NEGATIVE = 1234321
GEN_SEED_TRANSITION_MISMATCHED = 777  # check 5 (Adendo ao Gap (c) validation)

COMMON_GEN_KW = dict(mean_delay=0.02, duration=6000, max_cluster_size=3000, max_events=500000)

results = {}
t_start_all = time.time()

# --------------------------------------------------------------------------
# 1. Positive control: standalone critical branching process (tau_theory=1.5)
# --------------------------------------------------------------------------
print("=== 1. POSITIVE CONTROL (critical branching process, branching_ratio=1.0) ===")
rng = np.random.default_rng(GEN_SEED_POS)
ev_pos = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
lam_pos = compute_lambda(ev_pos)
t0 = time.time()
seg_pos = analyze_segment(ev_pos, lam_pos, do_mle_bootstrap=True,
                           n_mle_bootstrap=N_MLE_BOOTSTRAP, rng=np.random.default_rng(1))
dt_pos = time.time() - t0
print(f"  n_events={len(ev_pos)} lambda={lam_pos:.5f} n_avalanches={seg_pos['n_avalanches']} "
      f"tau={seg_pos['tau_fit']['tau']:.4f} D={seg_pos['tau_fit']['D']:.4f} "
      f"xmin={seg_pos['tau_fit']['xmin']} sigma={seg_pos['sigma']:.4f} "
      f"n_sigma_pairs={seg_pos['n_sigma_pairs']} time={dt_pos:.2f}s")
results["1_positive_control"] = {
    "description": "Standalone critical branching process (branching_ratio=1.0), "
                    "theoretical tau=1.5 (Borel/GW total-progeny asymptotics, Otter 1949/Dwass 1969)",
    "generator": {"model": "immigration-birth branching process (Hawkes cluster representation)",
                  "mu_immigrants": 0.05, "branching_ratio": 1.0, **COMMON_GEN_KW,
                  "gen_seed": GEN_SEED_POS},
    "n_events": int(len(ev_pos)), "lambda": lam_pos,
    "n_avalanches": seg_pos["n_avalanches"],
    "tau": seg_pos["tau_fit"]["tau"], "tau_xmin": seg_pos["tau_fit"]["xmin"],
    "tau_D": seg_pos["tau_fit"]["D"], "tau_n_tail": seg_pos["tau_fit"]["n_tail"],
    "tau_bootstrap_ci95": seg_pos["tau_bootstrap"]["tau_ci95"],
    "tau_bootstrap_std": seg_pos["tau_bootstrap"]["tau_std"],
    "sigma": seg_pos["sigma"], "n_sigma_pairs": seg_pos["n_sigma_pairs"],
    "compute_time_s": dt_pos,
}

# --------------------------------------------------------------------------
# 2. Negative control: standalone pure homogeneous Poisson process
# --------------------------------------------------------------------------
print("\n=== 2. NEGATIVE CONTROL (pure homogeneous Poisson, no clustering) ===")
rng = np.random.default_rng(GEN_SEED_NEG)
mu_neg = len(ev_pos) / (ev_pos.max() - ev_pos.min())  # rate-matched to the positive control for comparability
ev_neg = generate_homogeneous_poisson_events(rng, mu=mu_neg, duration=6000)
lam_neg = compute_lambda(ev_neg)
t0 = time.time()
seg_neg = analyze_segment(ev_neg, lam_neg, do_mle_bootstrap=True,
                           n_mle_bootstrap=N_MLE_BOOTSTRAP, rng=np.random.default_rng(2))
dt_neg = time.time() - t0
print(f"  n_events={len(ev_neg)} lambda={lam_neg:.5f} n_avalanches={seg_neg['n_avalanches']} "
      f"tau={seg_neg['tau_fit']['tau']:.4f} D={seg_neg['tau_fit']['D']:.4f} "
      f"xmin={seg_neg['tau_fit']['xmin']} sigma={seg_neg['sigma']:.4f} "
      f"n_sigma_pairs={seg_neg['n_sigma_pairs']} time={dt_neg:.2f}s")
results["2_negative_control"] = {
    "description": "Standalone pure homogeneous Poisson process (rate-matched to control 1's mean "
                    "rate) -- no clustering structure; checks the MLE/KS fit does not spuriously "
                    "recover a clean tau~1.5 power law where none exists.",
    "generator": {"model": "homogeneous Poisson", "mu": mu_neg, "duration": 6000, "gen_seed": GEN_SEED_NEG},
    "n_events": int(len(ev_neg)), "lambda": lam_neg,
    "n_avalanches": seg_neg["n_avalanches"],
    "tau": seg_neg["tau_fit"]["tau"], "tau_xmin": seg_neg["tau_fit"]["xmin"],
    "tau_D": seg_neg["tau_fit"]["D"], "tau_n_tail": seg_neg["tau_fit"]["n_tail"],
    "tau_bootstrap_ci95": seg_neg["tau_bootstrap"]["tau_ci95"],
    "tau_bootstrap_std": seg_neg["tau_bootstrap"]["tau_std"],
    "sigma": seg_neg["sigma"], "n_sigma_pairs": seg_neg["n_sigma_pairs"],
    "avalanche_T_distribution_note": "expected near-geometric run-length distribution for Poisson "
                                      "bin occupancy, not a clean power law",
    "compute_time_s": dt_neg,
}

# --------------------------------------------------------------------------
# 3. Transition control: PRE subcritical (0.5) -> POST critical (1.0)
#    mu_immigrants tuned so PRE/POST total event RATES are comparable
#    (avoids conflating a pure rate difference with the intended structural
#    difference -- see module docstring).
# --------------------------------------------------------------------------
print("\n=== 3. TRANSITION CONTROL (PRE subcritical 0.5 -> POST critical 1.0) ===")
rng = np.random.default_rng(GEN_SEED_TRANSITION)
pre_trans = generate_branching_events(rng, mu_immigrants=0.6, branching_ratio=0.5, **COMMON_GEN_KW)
post_trans = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
print(f"  pre n_events={len(pre_trans)}  post n_events={len(post_trans)}  "
      f"(rate pre={len(pre_trans)/6000:.3f}/t, rate post={len(post_trans)/6000:.3f}/t)")
t0 = time.time()
res_trans = run_soc_pipeline(pre_trans, post_trans, n_surrogates=N_SURROGATES,
                              n_mle_bootstrap=N_MLE_BOOTSTRAP)
dt_trans = time.time() - t0
print(f"  time={dt_trans:.1f}s lambda={res_trans['lambda']:.5f}")
print(f"  tau_pre={res_trans['tau_pre']:.4f} tau_post={res_trans['tau_post']:.4f} "
      f"delta_tau={res_trans['delta_tau']:.4f} p_tau={res_trans['p_tau']}")
print(f"  [PRIMARY] delta_tau_boot_ci95={res_trans['paired_bootstrap_tau']['delta_tau_boot_ci95']} "
      f"p_bootstrap_tau={res_trans['paired_bootstrap_tau']['p_bootstrap_tau']} "
      f"n_paired={res_trans['paired_bootstrap_tau']['n_paired']}")
print(f"  sigma_pre={res_trans['sigma_pre']:.4f} (n_pairs={res_trans['n_sigma_pairs_pre']}) "
      f"sigma_post={res_trans['sigma_post']:.4f} (n_pairs={res_trans['n_sigma_pairs_post']}) "
      f"delta_sigma={res_trans['delta_sigma']:.4f} p_sigma={res_trans['p_sigma']}")
print(f"  n_avalanches pre={res_trans['real_pre']['n_avalanches']} post={res_trans['real_post']['n_avalanches']}")
results["3_transition_control"] = {
    "description": "PRE=subcritical branching process (branching_ratio=0.5, mu_immigrants tuned "
                    "for comparable total event RATE to POST), POST=critical branching process "
                    "(branching_ratio=1.0, tau_theory=1.5). Real Delta_tau/Delta_sigma tested "
                    "against the N_SURROGATES=1000 homogeneous-Poisson surrogate null.",
    "generator": {"pre": {"mu_immigrants": 0.6, "branching_ratio": 0.5, **COMMON_GEN_KW},
                  "post": {"mu_immigrants": 0.05, "branching_ratio": 1.0, **COMMON_GEN_KW},
                  "gen_seed": GEN_SEED_TRANSITION},
    "n_events_pre": int(len(pre_trans)), "n_events_post": int(len(post_trans)),
    "lambda": res_trans["lambda"],
    "n_avalanches_pre": res_trans["real_pre"]["n_avalanches"],
    "n_avalanches_post": res_trans["real_post"]["n_avalanches"],
    "tau_pre": res_trans["tau_pre"], "tau_post": res_trans["tau_post"], "delta_tau": res_trans["delta_tau"],
    "tau_pre_xmin": res_trans["real_pre"]["tau_fit"]["xmin"],
    "tau_post_xmin": res_trans["real_post"]["tau_fit"]["xmin"],
    "tau_pre_D": res_trans["real_pre"]["tau_fit"]["D"], "tau_post_D": res_trans["real_post"]["tau_fit"]["D"],
    "p_tau": res_trans["p_tau"],
    "delta_tau_boot_ci95": res_trans["paired_bootstrap_tau"]["delta_tau_boot_ci95"],
    "p_bootstrap_tau": res_trans["paired_bootstrap_tau"]["p_bootstrap_tau"],
    "n_paired_bootstrap": res_trans["paired_bootstrap_tau"]["n_paired"],
    "delta_tau_boot_mean": res_trans["paired_bootstrap_tau"]["delta_tau_boot_mean"],
    "delta_tau_boot_std": res_trans["paired_bootstrap_tau"]["delta_tau_boot_std"],
    "sigma_pre": res_trans["sigma_pre"], "sigma_post": res_trans["sigma_post"],
    "delta_sigma": res_trans["delta_sigma"], "p_sigma": res_trans["p_sigma"],
    "n_sigma_pairs_pre": res_trans["n_sigma_pairs_pre"], "n_sigma_pairs_post": res_trans["n_sigma_pairs_post"],
    "n_surrogates_valid_tau": res_trans["n_surrogates_valid_tau"],
    "n_surrogates_valid_sigma": res_trans["n_surrogates_valid_sigma"],
    "surrogate_delta_tau_mean": res_trans["surrogate_delta_tau_mean"],
    "surrogate_delta_tau_std": res_trans["surrogate_delta_tau_std"],
    "surrogate_delta_sigma_mean": res_trans["surrogate_delta_sigma_mean"],
    "surrogate_delta_sigma_std": res_trans["surrogate_delta_sigma_std"],
    "robustness": res_trans["robustness"],
    "compute_time_s": dt_trans,
}

# --------------------------------------------------------------------------
# 4. Negative control for the surrogate-null test: PRE and POST independently
#    drawn from the SAME generative process (both critical, branching=1.0).
# --------------------------------------------------------------------------
print("\n=== 4. NEGATIVE CONTROL FOR NULL TEST (PRE=POST same critical process, independent draws) ===")
rng = np.random.default_rng(GEN_SEED_NULL_NEGATIVE)
pre_null = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
post_null = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
print(f"  pre n_events={len(pre_null)}  post n_events={len(post_null)}")
t0 = time.time()
res_null = run_soc_pipeline(pre_null, post_null, n_surrogates=N_SURROGATES,
                             n_mle_bootstrap=N_MLE_BOOTSTRAP)
dt_null = time.time() - t0
print(f"  time={dt_null:.1f}s lambda={res_null['lambda']:.5f}")
print(f"  tau_pre={res_null['tau_pre']:.4f} tau_post={res_null['tau_post']:.4f} "
      f"delta_tau={res_null['delta_tau']:.4f} p_tau={res_null['p_tau']}")
print(f"  [PRIMARY] delta_tau_boot_ci95={res_null['paired_bootstrap_tau']['delta_tau_boot_ci95']} "
      f"p_bootstrap_tau={res_null['paired_bootstrap_tau']['p_bootstrap_tau']} "
      f"n_paired={res_null['paired_bootstrap_tau']['n_paired']}")
print(f"  sigma_pre={res_null['sigma_pre']:.4f} (n_pairs={res_null['n_sigma_pairs_pre']}) "
      f"sigma_post={res_null['sigma_post']:.4f} (n_pairs={res_null['n_sigma_pairs_post']}) "
      f"delta_sigma={res_null['delta_sigma']:.4f} p_sigma={res_null['p_sigma']}")
print(f"  n_avalanches pre={res_null['real_pre']['n_avalanches']} post={res_null['real_post']['n_avalanches']}")
results["4_negative_control_null_test"] = {
    "description": "PRE and POST independently drawn from the SAME critical branching process "
                    "(branching_ratio=1.0 for both) -- structurally null case; checks the "
                    "Poisson-surrogate test does not spuriously flag a genuinely-null transition.",
    "generator": {"pre": {"mu_immigrants": 0.05, "branching_ratio": 1.0, **COMMON_GEN_KW},
                  "post": {"mu_immigrants": 0.05, "branching_ratio": 1.0, **COMMON_GEN_KW},
                  "gen_seed": GEN_SEED_NULL_NEGATIVE},
    "n_events_pre": int(len(pre_null)), "n_events_post": int(len(post_null)),
    "lambda": res_null["lambda"],
    "n_avalanches_pre": res_null["real_pre"]["n_avalanches"],
    "n_avalanches_post": res_null["real_post"]["n_avalanches"],
    "tau_pre": res_null["tau_pre"], "tau_post": res_null["tau_post"], "delta_tau": res_null["delta_tau"],
    "p_tau": res_null["p_tau"],
    "delta_tau_boot_ci95": res_null["paired_bootstrap_tau"]["delta_tau_boot_ci95"],
    "p_bootstrap_tau": res_null["paired_bootstrap_tau"]["p_bootstrap_tau"],
    "n_paired_bootstrap": res_null["paired_bootstrap_tau"]["n_paired"],
    "delta_tau_boot_mean": res_null["paired_bootstrap_tau"]["delta_tau_boot_mean"],
    "delta_tau_boot_std": res_null["paired_bootstrap_tau"]["delta_tau_boot_std"],
    "sigma_pre": res_null["sigma_pre"], "sigma_post": res_null["sigma_post"],
    "delta_sigma": res_null["delta_sigma"], "p_sigma": res_null["p_sigma"],
    "n_sigma_pairs_pre": res_null["n_sigma_pairs_pre"], "n_sigma_pairs_post": res_null["n_sigma_pairs_post"],
    "n_surrogates_valid_tau": res_null["n_surrogates_valid_tau"],
    "n_surrogates_valid_sigma": res_null["n_surrogates_valid_sigma"],
    "compute_time_s": dt_null,
}

# --------------------------------------------------------------------------
# 4b. Repeatability check on the negative-control p_sigma (a single p_sigma=
#     0.024 was observed in exploratory testing for this exact scenario type
#     -- borderline-significant despite PRE/POST being structurally
#     identical by construction. Two more independent repeats, run with a
#     cheaper N_MLE_BOOTSTRAP since only the surrogate-test p-values matter
#     here, to check whether this was a single ~5%-level false positive
#     (expected occasionally at alpha=0.05) or a systematic miscalibration.)
# --------------------------------------------------------------------------
print("\n=== 4b. Repeatability check: 2 more independent null-negative-control draws ===")
repeat_seeds = [222222, 333333]
repeats = []
for rseed in repeat_seeds:
    rng = np.random.default_rng(rseed)
    pre_r = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
    post_r = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
    t0 = time.time()
    res_r = run_soc_pipeline(pre_r, post_r, n_surrogates=N_SURROGATES, n_mle_bootstrap=50,
                              compute_robustness=False)
    dt_r = time.time() - t0
    print(f"  seed={rseed} time={dt_r:.1f}s tau_pre={res_r['tau_pre']:.3f} tau_post={res_r['tau_post']:.3f} "
          f"p_tau={res_r['p_tau']} p_bootstrap_tau={res_r['paired_bootstrap_tau']['p_bootstrap_tau']} "
          f"sigma_pre={res_r['sigma_pre']:.3f} sigma_post={res_r['sigma_post']:.3f} "
          f"p_sigma={res_r['p_sigma']}")
    repeats.append({
        "gen_seed": rseed, "tau_pre": res_r["tau_pre"], "tau_post": res_r["tau_post"],
        "delta_tau": res_r["delta_tau"], "p_tau": res_r["p_tau"],
        "delta_tau_boot_ci95": res_r["paired_bootstrap_tau"]["delta_tau_boot_ci95"],
        "p_bootstrap_tau": res_r["paired_bootstrap_tau"]["p_bootstrap_tau"],
        "n_paired_bootstrap": res_r["paired_bootstrap_tau"]["n_paired"],
        "sigma_pre": res_r["sigma_pre"], "sigma_post": res_r["sigma_post"],
        "delta_sigma": res_r["delta_sigma"], "p_sigma": res_r["p_sigma"],
        "n_avalanches_pre": res_r["real_pre"]["n_avalanches"], "n_avalanches_post": res_r["real_post"]["n_avalanches"],
        "compute_time_s": dt_r,
    })
results["4b_null_negative_control_repeats"] = {
    "description": "Two additional independent PRE=POST-same-critical-process draws "
                    "(n_mle_bootstrap reduced to 50 here since only p_tau/p_sigma from the "
                    "surrogate loop, and p_bootstrap_tau from the (coarser, 50-pair) paired-bootstrap "
                    "test, are needed, not tau's own tightly-resolved CI) -- checks whether the "
                    "p_sigma=0.024 observed in run 4 was an isolated ~5%-level false positive or "
                    "systematic, and whether p_bootstrap_tau is similarly well-calibrated under the null.",
    "runs": repeats,
    "p_sigma_values_across_all_3_null_negative_runs": [results["4_negative_control_null_test"]["p_sigma"]] +
                                                        [r["p_sigma"] for r in repeats],
    "p_tau_values_across_all_3_null_negative_runs": [results["4_negative_control_null_test"]["p_tau"]] +
                                                      [r["p_tau"] for r in repeats],
    "p_bootstrap_tau_values_across_all_3_null_negative_runs":
        [results["4_negative_control_null_test"]["p_bootstrap_tau"]] +
        [r["p_bootstrap_tau"] for r in repeats],
}

# --------------------------------------------------------------------------
# 5. TRANSITION CONTROL, RATE-MISMATCHED (Adendo ao Gap (c) validation): the
#    SAME branching_ratio difference as check 3 (PRE subcritical 0.5 -> POST
#    critical 1.0), but WITHOUT check 3's mu_immigrants tuning that
#    equalizes total PRE/POST event rate -- both segments use the SAME
#    mu_immigrants=0.05 here, so the rate mismatch comes purely from how
#    much branching amplifies event count differently at branching_ratio=0.5
#    (subcritical, mean cluster size finite = 1/(1-0.5)=2) vs 1.0 (critical,
#    mean cluster size formally divergent, realized value large under the
#    shared max_cluster_size truncation) -- exactly the "few background
#    events before the mainshock, many in the aftershock sequence" real-world
#    mechanism METHODOLOGY_NOTE.md's Adendo names as the motivating risk.
#    This reproduces the scenario class that gave p_tau=0.285 under the
#    Poisson-surrogate test alone (documented in the Adendo); confirms
#    p_bootstrap_tau recovers power.
# --------------------------------------------------------------------------
print("\n=== 5. TRANSITION CONTROL, RATE-MISMATCHED (same branching_ratio 0.5->1.0, "
      "mu_immigrants NOT tuned for equal rate) ===")
rng = np.random.default_rng(GEN_SEED_TRANSITION_MISMATCHED)
pre_mm = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=0.5, **COMMON_GEN_KW)
post_mm = generate_branching_events(rng, mu_immigrants=0.05, branching_ratio=1.0, **COMMON_GEN_KW)
print(f"  pre n_events={len(pre_mm)}  post n_events={len(post_mm)}  "
      f"(rate pre={len(pre_mm)/6000:.4f}/t, rate post={len(post_mm)/6000:.4f}/t, "
      f"rate ratio post/pre={ (len(post_mm)/6000) / (len(pre_mm)/6000):.1f}x)")
t0 = time.time()
res_mm = run_soc_pipeline(pre_mm, post_mm, n_surrogates=N_SURROGATES,
                           n_mle_bootstrap=N_MLE_BOOTSTRAP)
dt_mm = time.time() - t0
print(f"  time={dt_mm:.1f}s lambda={res_mm['lambda']:.5f}")
print(f"  tau_pre={res_mm['tau_pre']:.4f} tau_post={res_mm['tau_post']:.4f} "
      f"delta_tau={res_mm['delta_tau']:.4f}")
print(f"  [SECONDARY, Poisson surrogate] p_tau={res_mm['p_tau']}")
print(f"  [PRIMARY, paired bootstrap] delta_tau_boot_ci95={res_mm['paired_bootstrap_tau']['delta_tau_boot_ci95']} "
      f"p_bootstrap_tau={res_mm['paired_bootstrap_tau']['p_bootstrap_tau']} "
      f"n_paired={res_mm['paired_bootstrap_tau']['n_paired']}")
print(f"  sigma_pre={res_mm['sigma_pre']:.4f} (n_pairs={res_mm['n_sigma_pairs_pre']}) "
      f"sigma_post={res_mm['sigma_post']:.4f} (n_pairs={res_mm['n_sigma_pairs_post']}) "
      f"delta_sigma={res_mm['delta_sigma']:.4f} p_sigma={res_mm['p_sigma']}")
print(f"  n_avalanches pre={res_mm['real_pre']['n_avalanches']} post={res_mm['real_post']['n_avalanches']}")
results["5_transition_control_rate_mismatched"] = {
    "description": "Adendo ao Gap (c) validation: same branching_ratio difference as check 3 "
                    "(PRE=0.5 subcritical, POST=1.0 critical) but mu_immigrants NOT tuned for equal "
                    "PRE/POST rate (both 0.05) -- reproduces the large-rate-mismatch scenario class "
                    "documented in METHODOLOGY_NOTE.md as giving p_tau=0.285 under the "
                    "Poisson-surrogate test alone despite a large real Delta_tau. Confirms "
                    "p_bootstrap_tau (PRIMARY test) recovers power where p_tau (SECONDARY test) does not.",
    "generator": {"pre": {"mu_immigrants": 0.05, "branching_ratio": 0.5, **COMMON_GEN_KW},
                  "post": {"mu_immigrants": 0.05, "branching_ratio": 1.0, **COMMON_GEN_KW},
                  "gen_seed": GEN_SEED_TRANSITION_MISMATCHED},
    "n_events_pre": int(len(pre_mm)), "n_events_post": int(len(post_mm)),
    "rate_pre": float(len(pre_mm) / 6000), "rate_post": float(len(post_mm) / 6000),
    "rate_ratio_post_over_pre": float((len(post_mm) / 6000) / (len(pre_mm) / 6000)),
    "lambda": res_mm["lambda"],
    "n_avalanches_pre": res_mm["real_pre"]["n_avalanches"],
    "n_avalanches_post": res_mm["real_post"]["n_avalanches"],
    "tau_pre": res_mm["tau_pre"], "tau_post": res_mm["tau_post"], "delta_tau": res_mm["delta_tau"],
    "tau_pre_xmin": res_mm["real_pre"]["tau_fit"]["xmin"],
    "tau_post_xmin": res_mm["real_post"]["tau_fit"]["xmin"],
    "tau_pre_D": res_mm["real_pre"]["tau_fit"]["D"], "tau_post_D": res_mm["real_post"]["tau_fit"]["D"],
    "p_tau_poisson_surrogate_SECONDARY": res_mm["p_tau"],
    "delta_tau_boot_ci95": res_mm["paired_bootstrap_tau"]["delta_tau_boot_ci95"],
    "p_bootstrap_tau_PRIMARY": res_mm["paired_bootstrap_tau"]["p_bootstrap_tau"],
    "n_paired_bootstrap": res_mm["paired_bootstrap_tau"]["n_paired"],
    "delta_tau_boot_mean": res_mm["paired_bootstrap_tau"]["delta_tau_boot_mean"],
    "delta_tau_boot_std": res_mm["paired_bootstrap_tau"]["delta_tau_boot_std"],
    "sigma_pre": res_mm["sigma_pre"], "sigma_post": res_mm["sigma_post"],
    "delta_sigma": res_mm["delta_sigma"], "p_sigma": res_mm["p_sigma"],
    "n_sigma_pairs_pre": res_mm["n_sigma_pairs_pre"], "n_sigma_pairs_post": res_mm["n_sigma_pairs_post"],
    "n_surrogates_valid_tau": res_mm["n_surrogates_valid_tau"],
    "n_surrogates_valid_sigma": res_mm["n_surrogates_valid_sigma"],
    "surrogate_delta_tau_mean": res_mm["surrogate_delta_tau_mean"],
    "surrogate_delta_tau_std": res_mm["surrogate_delta_tau_std"],
    "robustness": res_mm["robustness"],
    "compute_time_s": dt_mm,
}

results["_config"] = {
    "N_SURROGATES": N_SURROGATES, "N_MLE_BOOTSTRAP": N_MLE_BOOTSTRAP,
    "pipeline_internal_seed": SEED,
    "total_compute_time_s": time.time() - t_start_all,
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validation_synthetic.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nTotal validation compute time: {results['_config']['total_compute_time_s']:.1f}s")
print(f"Wrote {out_path}")
