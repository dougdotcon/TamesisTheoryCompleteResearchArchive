"""
ref_common.py -- referee's own independent measurement code for the
long_cycle_deficit_attempt front. Written from scratch from the prose
methodology in DERIVATION_PREREG.md (this front's pre-registration) and
sc_engine.py's own API/docstrings (short_cycle_dynamics_attempt, the parent
front, already adversarially verified SOUND). Does NOT read or import
lcd_diagnostic.py or lcd_bsweep.py (this front's own new, untrusted scripts).

Measurement definition (re-derived independently, matching the prereg's
stated quantity): for a fixed (n, b, c) instance and an absolute L-threshold,

    phi_far = P(x0 is cyclic in f | x0 in R^c, L_pi(x0) > threshold)

estimated by pooling, across N independent instances, the count of
qualifying points (x0 in R^c, pi-cycle length > threshold) that are cyclic,
divided by the total count of qualifying points. Because points within one
instance are correlated (shared pi, shared R, shared f), the standard error
is computed two independent ways that must agree:

  (a) ratio-estimator delta method (Cochran-style, cluster = instance):
        phat = sum(Y_i) / sum(n_i),  Y_i = #qualifying-and-cyclic in inst i,
        n_i = #qualifying in inst i
        Var(phat) ~= (1/(N * xbar^2)) * (1/(N-1)) * sum_i (Y_i - phat*n_i)^2
        where xbar = mean(n_i)
  (b) cluster bootstrap: resample instances with replacement, B times,
      recompute pooled ratio each time, take std of the bootstrap
      distribution.

Both are reported; if they disagree badly that itself would be a finding.
"""
import sys
import numpy as np
from multiprocessing import Pool

PARENT_DIR = ("/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/"
              "02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/"
              "mclust_rigor/residual_attempt/aggregation_closure_attempt/"
              "global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/"
              "short_cycle_dynamics_attempt")
sys.path.insert(0, PARENT_DIR)
import sc_engine  # noqa: E402  (parent front's adversarially-verified engine, imported per mandate)
import sc_formula as F  # noqa: E402


def _one_instance(args):
    """Worker: build one instance, return (n_qualify, n_cyclic_qualify, n_R, n_R_measured)."""
    n, b, c, threshold, seed_int = args
    rng = np.random.default_rng(seed_int)
    inst = sc_engine.build_instance(n, b, c, rng)
    pi, R_mask, f = inst["pi"], inst["R_mask"], inst["f"]
    cyc_len = sc_engine.pi_cycle_lengths(pi)
    cyclic_mask = sc_engine.cyclic_mask_peeling(f)
    Rc_mask = ~R_mask
    qualify = Rc_mask & (cyc_len > threshold)
    n_q = int(qualify.sum())
    n_cq = int((qualify & cyclic_mask).sum())
    n_R = int(R_mask.sum())
    return n_q, n_cq, n_R


def run_cell(n, b, c, threshold, N, seed_base, n_workers=4, label=""):
    """Run N instances (fresh independent RNG streams via SeedSequence.spawn),
    pool the qualifying-point counts, compute phi_far, delta-method SE, and a
    cluster bootstrap SE. Returns a dict of results."""
    ss = np.random.SeedSequence(seed_base)
    children = ss.spawn(N)
    seed_ints = [int(c_.generate_state(1)[0]) for c_ in children]
    args = [(n, b, c, threshold, s) for s in seed_ints]

    with Pool(n_workers) as pool:
        results = pool.map(_one_instance, args, chunksize=max(1, N // (n_workers * 8)))

    n_q = np.array([r[0] for r in results], dtype=np.int64)
    n_cq = np.array([r[1] for r in results], dtype=np.int64)
    n_R = np.array([r[2] for r in results], dtype=np.int64)

    total_q = n_q.sum()
    total_cq = n_cq.sum()
    phat = total_cq / total_q if total_q > 0 else float("nan")

    # (a) delta-method ratio-estimator SE (cluster = instance)
    xbar = n_q.mean()
    resid = n_cq - phat * n_q
    var_delta = (np.sum(resid ** 2) / (N - 1)) / (N * xbar ** 2)
    se_delta = np.sqrt(var_delta)

    # (b) cluster bootstrap
    rng_boot = np.random.default_rng(seed_base + 999999999)
    B = 2000
    idx_all = np.arange(N)
    boot_phats = np.empty(B)
    for k in range(B):
        idx = rng_boot.integers(0, N, size=N)
        bq = n_q[idx].sum()
        bcq = n_cq[idx].sum()
        boot_phats[k] = bcq / bq if bq > 0 else np.nan
    se_boot = np.nanstd(boot_phats, ddof=1)

    rho_measured = n_R.mean() / n
    rho_formula = F.rho_of(b, c, n)

    out = dict(
        label=label, n=n, b=b, c=c, threshold=threshold, N=N, seed_base=seed_base,
        total_q=int(total_q), total_cq=int(total_cq),
        phi_far=phat, se_delta=se_delta, se_boot=se_boot,
        rho_measured=rho_measured, rho_formula=rho_formula,
    )
    return out


def phi_ref(b, c, n):
    """phi_U(c'') -- the reference the front compares against."""
    cpp = F.c_double_prime(b, c, n)
    return F.phi_U(cpp)


def report_line(res, phiU):
    phi_far = res["phi_far"]
    se_d = res["se_delta"]
    se_b = res["se_boot"]
    dev_d = 100 * (phi_far - phiU) / phiU
    z_d = (phi_far - phiU) / se_d
    z_b = (phi_far - phiU) / se_b
    return (f"[{res['label']}] n={res['n']} b={res['b']} c={res['c']} thr={res['threshold']} "
            f"N={res['N']} seed={res['seed_base']}\n"
            f"  total_qualify={res['total_q']:,}  total_cyclic_qualify={res['total_cq']:,}\n"
            f"  rho_measured={res['rho_measured']:.5f}  rho_formula={res['rho_formula']:.5f}\n"
            f"  phi_far = {phi_far:.6f}\n"
            f"  SE(delta-method) = {se_d:.6f}   SE(cluster-bootstrap,B=2000) = {se_b:.6f}"
            f"   ratio={se_b/se_d:.3f}\n"
            f"  phi_U(c'') = {phiU:.6f}\n"
            f"  dev% (delta SE)   = {dev_d:+.3f}%   z (delta)    = {z_d:+.3f}\n"
            f"  dev% (boot SE)    = {dev_d:+.3f}%   z (boot)     = {z_b:+.3f}\n")
