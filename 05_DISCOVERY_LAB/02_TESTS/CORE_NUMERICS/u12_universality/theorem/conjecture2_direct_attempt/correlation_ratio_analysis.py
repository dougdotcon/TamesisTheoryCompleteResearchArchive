"""
Post-processing of two_point_exploration_mc_c{1,4}_results.json: compute
the normalized correlation ratio

    rho(ell) := (g(ell) - marg(ell)^2) / (marg(ell) - marg(ell)^2)

using the TRUE empirical finite-n marginal (not the continuum guessA),
where g(ell)=P(both cyclic|same cycle,ell) and marg(ell)=P(one
cyclic|own cycle length=ell) [both empirical, from the bucket_rows /
marginal_bucket_rows of the MC]. rho=0 would mean the two points'
cyclic statuses are (given ell) as good as independent; rho=1 would
mean they are perfectly coupled ("same fate"). This makes the
qualitative pattern seen in the two raw MC logs (c=1, c=4) precise and
comparable across c.

NUMERICALLY EXPLORED, not proof -- see DERIVATION_PREREG.md.
"""
import json

for c, fname in [(1.0, "two_point_exploration_mc_c1_results.json"),
                  (4.0, "two_point_exploration_mc_c4_results.json")]:
    with open(fname) as fh:
        d = json.load(fh)
    g_rows = {round(r["ell_mid"], 3): r["empirical_g"] for r in d["bucket_rows"]}
    m_rows = {round(r["ell_mid"], 3): r["empirical_marginal"] for r in d["marginal_bucket_rows"]}
    print(f"\n=== c={c} ===")
    print(f"{'ell_mid':>8} {'marg':>8} {'marg^2':>8} {'g':>8} {'rho':>8}")
    for k in sorted(g_rows):
        if k not in m_rows:
            continue
        marg = m_rows[k]
        g = g_rows[k]
        denom = marg - marg**2
        rho = (g - marg**2) / denom if denom > 1e-9 else float('nan')
        print(f"{k:8.3f} {marg:8.4f} {marg**2:8.4f} {g:8.4f} {rho:8.4f}")
