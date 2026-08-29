#!/usr/bin/env python3
"""
adv01_independent_reconstruction.py

HOSTILE REFEREE, INDEPENDENT VERIFICATION of
gap_rate_candidate_attempt/ATTEMPT.md (MCLUST-GAP-RATE-CANDIDATE-ATTEMPT,
wave 25 front (d), DISC-DEC-118).

Written FROM SCRATCH (no line copied from r01_reconstruct_and_crosscheck.py
/ r02_power_law_fit.py / r03_perbin_and_exploratory.py, which were not
opened until after this script's first version ran and its numbers were
compared to the target document's claims) before the target front's own
scripts were read. All bin data below (T1, T2-composite, Pi_abstract) was
transcribed directly by the referee from reading
`mclust_plateau_abstract_real_gap_attempt/ATTEMPT.md` SS A.1/A.2 (the
parent front the target document cites), not from the target's own
scripts. Plain stdlib only (math, json) -- no numpy/scipy, so every
formula below is manual and auditable line-by-line.

Purpose: independently re-derive every headline number in the target
ATTEMPT.md (structural degeneracy, magnitude-fit prefactors and
residuals, exact-unit-prefactor exponent p*, Pearson r(gap,t0), and the
exploratory n_eff(t0) extension) and confirm or refute them.
"""
import math
import json

# ---------------------------------------------------------------------
# 1. Data, transcribed BY THE REFEREE from the parent front's ATTEMPT.md
#    SS A.2 (read directly by the referee -- see REFEREE_REPORT.md SS1 for
#    the exact lines quoted).
# ---------------------------------------------------------------------

# Table T1 (absolute-ell bins): (t0 mid/n, published gap%)
T1 = [
    (0.011, 26.72),
    (0.046, 42.50),
    (0.092, 49.26),
    (0.186, 46.36),
    (0.375, 41.96),
    (0.750, 38.32),
]

# Table T2-composite (relative L/n bins, cluster-robust at bins 8,9):
# (t0 mid, published gap%)
T2 = [
    (0.046, 35.78),
    (0.091, 39.03),
    (0.186, 37.46),
    (0.312, 41.27),
    (0.438, 38.73),
    (0.562, 35.78),
    (0.688, 40.27),
    (0.812, 43.20),
    (0.938, 37.46),
]

c = 1000.0
n = 65536.0


def mean(xs):
    return sum(xs) / len(xs)


def rms(residuals):
    return math.sqrt(sum(r * r for r in residuals) / len(residuals))


def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny)


def generic_ols_single_regressor(x_list, y_list):
    """Standard no-intercept OLS for y = A*x, general x_i (may vary bin to
    bin). Used both as a sanity check against the closed form (when x_i is
    constant) and as the REAL fit for the n_eff(t0) extension (where x_i
    genuinely varies)."""
    sx2 = sum(x * x for x in x_list)
    sxy = sum(x * y for x, y in zip(x_list, y_list))
    return sxy / sx2


# ---------------------------------------------------------------------
# 2. Structural-degeneracy claim: c,n fixed => (c/n)^p is ONE number.
# ---------------------------------------------------------------------

cn = c / n
print(f"c/n = {cn!r}")
print(f"exact-fraction cross-check: 1000/65536 = {1000/65536!r}, "
      f"125/8192 = {125/8192!r}")
assert abs(cn - 125 / 8192) < 1e-18, "c/n arithmetic mismatch"

rates = {}
for p, label in [(1 / 2, "1/2"), (1 / 3, "1/3"), (1 / 4, "1/4"), (1 / 5, "1/5")]:
    rates[label] = cn ** p
    print(f"(c/n)^({label}) = {rates[label]*100:.6f}%")

rate_1_over_n = 1.0 / n
rate_1_over_sqrtn = 1.0 / math.sqrt(n)
print(f"1/n            = {rate_1_over_n*100:.6f}%")
print(f"1/sqrt(n)      = {rate_1_over_sqrtn*100:.6f}%")

# ---------------------------------------------------------------------
# 3. Magnitude-only fit report per table, per exponent.
# ---------------------------------------------------------------------

def report_table(name, table, rates):
    t0s = [t for t, g in table]
    gaps = [g for t, g in table]
    m = mean(gaps)
    print(f"\n=== {name} ===  n_bins={len(table)}  mean(gap)={m:.4f}%")
    for label in ["1/3", "1/4", "1/5"]:
        rate = rates[label]
        x_list = [rate] * len(table)  # CONSTANT regressor: the crux of the claim
        A_closed = m / rate
        A_generic = generic_ols_single_regressor(x_list, gaps)
        assert abs(A_closed - A_generic) < 1e-9, (
            "closed-form vs generic-OLS mismatch -- degeneracy claim false!"
        )
        preds = [A_closed * rate for _ in table]
        resids = [g - pred for g, pred in zip(gaps, preds)]
        r_rms = rms(resids)
        r_max = max(abs(r) for r in resids)
        direct_resids = [g - m for g in gaps]
        max_diff_from_direct = max(
            abs(a - b) for a, b in zip(resids, direct_resids)
        )
        nat_resids = [g - rate * 100 for g in gaps]
        nat_rms = rms(nat_resids)
        print(
            f"  p={label}: rate={rate*100:.4f}%  A*={A_closed:.4f}  "
            f"|A*-1|={abs(A_closed-1):.4f}  RMS_resid={r_rms:.4f}pp  "
            f"max|resid|={r_max:.4f}pp  natural(A=1)_RMS={nat_rms:.4f}pp  "
            f"(max diff vs (gap-mean): {max_diff_from_direct:.2e})"
        )
    return m


m_t1 = report_table("T1", T1, rates)
m_t2 = report_table("T2-composite", T2, rates)

# ---------------------------------------------------------------------
# 4. Exact-unit-prefactor exponent p*.
# ---------------------------------------------------------------------

def solve_pstar(mean_gap_pct, cn):
    target = mean_gap_pct / 100.0
    return math.log(target) / math.log(cn)

pstar_t1 = solve_pstar(m_t1, cn)
pstar_t2 = solve_pstar(m_t2, cn)
print(f"\np* (T1) = {pstar_t1:.6f}  1/p* = {1/pstar_t1:.4f}   "
      f"check: (c/n)^p* *100 = {cn**pstar_t1*100:.4f}% (should == {m_t1:.4f}%)")
print(f"p* (T2) = {pstar_t2:.6f}  1/p* = {1/pstar_t2:.4f}   "
      f"check: (c/n)^p* *100 = {cn**pstar_t2*100:.4f}% (should == {m_t2:.4f}%)")

# ---------------------------------------------------------------------
# 5. Pearson r(gap, t0).
# ---------------------------------------------------------------------

r_t1 = pearson([t for t, g in T1], [g for t, g in T1])
r_t2 = pearson([t for t, g in T2], [g for t, g in T2])
print(f"\nPearson r(gap,t0):  T1 = {r_t1:.4f}   T2-composite = {r_t2:.4f}")

# ---------------------------------------------------------------------
# 6. Exploratory n_eff(t0) = n*(1-t0) extension: genuine (non-degenerate)
#    fit, since x_i now varies bin-to-bin.
# ---------------------------------------------------------------------

def report_neff(name, table, p, label):
    t0s = [t for t, g in table]
    gaps = [g for t, g in table]
    m = mean(gaps)
    x_list = [(c / (n * (1 - t0))) ** p * 100 for t0 in t0s]
    A = generic_ols_single_regressor(x_list, gaps)
    preds = [A * x for x in x_list]
    resids = [g - pred for g, pred in zip(gaps, preds)]
    ss_res = sum(r * r for r in resids)
    ss_tot_flat = sum((g - m) ** 2 for g in gaps)
    R2 = 1 - ss_res / ss_tot_flat
    r_rms = rms(resids)
    r_max = max(abs(r) for r in resids)
    print(
        f"  n_eff, p={label}, {name}: A={A:.4f}  RMS_resid={r_rms:.3f}pp  "
        f"max|resid|={r_max:.3f}pp  R^2(vs flat mean)={R2:.3f}"
    )
    return t0s, gaps, x_list, preds, A


print("\n=== Exploratory n_eff(t0)=n(1-t0) extension ===")
for label, p in [("1/3", 1 / 3), ("1/4", 1 / 4), ("1/5", 1 / 5)]:
    for name, table in [("T1", T1), ("T2-composite", T2)]:
        report_neff(name, table, p, label)

# Spot check: T2 last bin (t0=0.938), p=1/4 -- compare against target's
# claimed "predicted 58.0% ... a -20.55pp miss".
t0 = 0.938
p = 0.25
n_eff = n * (1 - t0)
rate_eff_pct = (c / n_eff) ** p * 100
_, _, _, _, A_t2_p14 = report_neff("T2-composite (spot check refit)", T2, p, "1/4")
pred_last_bin = A_t2_p14 * rate_eff_pct
observed_last_bin = 37.46
print(f"\nSpot check T2 last bin (t0={t0}), p=1/4:")
print(f"  n_eff = n*(1-t0) = {n_eff:.2f}")
print(f"  raw rate_eff (unscaled) = {rate_eff_pct:.4f}%")
print(f"  fitted A = {A_t2_p14:.4f}")
print(f"  predicted = A * rate_eff = {pred_last_bin:.4f}%  "
      f"(target claims '58.0%')")
print(f"  observed = {observed_last_bin}%")
print(f"  miss = observed - predicted = {observed_last_bin - pred_last_bin:.4f}pp  "
      f"(target claims '-20.55pp miss')")

# ---------------------------------------------------------------------
# 7. Transcription cross-check: recompute gap% from phi_real using full
#    Decimal precision, independent of the target's own r01 script.
# ---------------------------------------------------------------------

from decimal import Decimal, getcontext
getcontext().prec = 50

PI = Decimal("0.0377615983402126188243712025905770479904")

T1_phi = [Decimal("0.0298"), Decimal("0.0265"), Decimal("0.0253"),
          Decimal("0.0258"), Decimal("0.0266"), Decimal("0.0273")]
T1_pub = [26.72, 42.50, 49.26, 46.36, 41.96, 38.32]

T2_phi = [Decimal("0.02781"), Decimal("0.02716"), Decimal("0.02747"),
          Decimal("0.02673"), Decimal("0.02722"), Decimal("0.02781"),
          Decimal("0.02692"), Decimal("0.02637"), Decimal("0.02747")]
T2_pub = [35.78, 39.03, 37.46, 41.27, 38.73, 35.78, 40.27, 43.20, 37.46]

print("\n=== Transcription cross-check (Decimal, independent of target's r01) ===")
max_disc = Decimal(0)
for label, phis, pubs in [("T1", T1_phi, T1_pub), ("T2", T2_phi, T2_pub)]:
    tbl_max = Decimal(0)
    for phi, pub in zip(phis, pubs):
        gap = (PI - phi) / phi * 100
        d = abs(gap - Decimal(str(pub)))
        tbl_max = max(tbl_max, d)
        max_disc = max(max_disc, d)
    print(f"  {label}: max |recomputed - published| = {tbl_max:.6f}pp")
print(f"  OVERALL max discrepancy = {max_disc:.6f}pp  "
      f"(target claims '0.0049pp')")

# ---------------------------------------------------------------------
# 8. Save results
# ---------------------------------------------------------------------

results = {
    "cn": cn,
    "rates": rates,
    "T1_mean_gap": m_t1,
    "T2_mean_gap": m_t2,
    "pstar_T1": pstar_t1,
    "pstar_T2": pstar_t2,
    "pearson_r_T1": r_t1,
    "pearson_r_T2": r_t2,
    "transcription_max_discrepancy_pp": float(max_disc),
}
with open("adv01_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nDone. Saved adv01_results.json")
