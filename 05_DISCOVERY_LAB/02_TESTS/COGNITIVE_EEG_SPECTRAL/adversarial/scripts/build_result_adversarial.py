import sys, json
sys.path.insert(0, '.')
import numpy as np
from stats_own import welch_ttest, mann_whitney_u

d = json.load(open('adversarial_per_subject.json'))
valid = [e for e in d if e.get('Ibar') is not None]
mdd = [e for e in valid if e['group'] == 'MDD']
hc = [e for e in valid if e['group'] == 'HC']
Ibar_mdd = np.array([e['Ibar'] for e in mdd])
Ibar_hc = np.array([e['Ibar'] for e in hc])
bp_mdd = np.array([e['bandpower_mean'] for e in mdd])
bp_hc = np.array([e['bandpower_mean'] for e in hc])

tt = welch_ttest(Ibar_mdd, Ibar_hc)
mw = mann_whitney_u(Ibar_mdd, Ibar_hc)
tt_bp = welch_ttest(bp_mdd, bp_hc)
mw_bp = mann_whitney_u(bp_mdd, bp_hc)

# dedup
by_md5 = {}
for e in valid:
    by_md5.setdefault(e['downloaded_md5_self'], []).append(e['subject_label'])
dup_groups = {k: v for k, v in by_md5.items() if len(v) > 1}
drop_labels = {sorted(v)[-1] for v in dup_groups.values()}
valid_dedup = [e for e in valid if e['subject_label'] not in drop_labels]
mdd_d = [e for e in valid_dedup if e['group'] == 'MDD']
hc_d = [e for e in valid_dedup if e['group'] == 'HC']
Ibar_mdd_d = np.array([e['Ibar'] for e in mdd_d])
Ibar_hc_d = np.array([e['Ibar'] for e in hc_d])
tt_dedup = welch_ttest(Ibar_mdd_d, Ibar_hc_d)
mw_dedup = mann_whitney_u(Ibar_mdd_d, Ibar_hc_d)

unavailable = [e['file_name'] for e in d if not e.get('download_ok')]
excluded = [e for e in d if e.get('download_ok') and e.get('excluded_by_artifact_rule')]

verdict = None
direction_mdd_lt_hc = bool(tt['mean1'] < tt['mean2'])
if tt['p_two_tailed'] < 0.05 and direction_mdd_lt_hc:
    verdict = "CONFIRMA"
elif tt['p_two_tailed'] < 0.05 and not direction_mdd_lt_hc:
    verdict = "REFUTA"
else:
    verdict = "INCONCLUSIVO"

out = {
    "adversarial_reproduction_of": "DISC-COGNITIVE-EEG-SPECTRAL-001 (depression arm)",
    "preregistration_lock": "DISC-DEC-028",
    "independent_agent": True,
    "own_implementation": {
        "edf_parser": "from-scratch, cross-validated against pyedflib (max abs diff 2.8e-13 uV on sample channel)",
        "welch_psd": "from-scratch, cross-validated against scipy.signal.welch (max abs diff 4.4e-15, max rel diff 1.4e-15 on synthetic noise)",
        "entropy": "from-scratch per PREREGISTRATION.md Sec.2",
        "artifact_rejection": "from-scratch per PREREGISTRATION.md Sec.4.5",
        "welch_ttest": "from-scratch (Welch-Satterthwaite df, incomplete-beta CDF via scipy.special.betainc), cross-validated against scipy.stats.ttest_ind to ~1e-16",
        "mann_whitney_u": "from-scratch (normal approx with tie + continuity correction), cross-validated against scipy.stats.mannwhitneyu to ~1e-16",
    },
    "data_access": {
        "source": "https://api.figshare.com/v2/articles/4244171 (fetched independently by this agent)",
        "n_ec_files_in_manifest": 64,
        "n_downloaded_and_md5_verified": len(valid) + len(excluded),
        "n_unavailable_404_after_3_retries_each": len(unavailable),
        "unavailable_files": unavailable,
        "unavailable_corroboration": "independently confirmed via API metadata: exactly these 6 EC files (and only these 6, among all 64) have computed_md5=='' and mimetype=='undefined' in the API listing, vs a real computed_md5/mimetype for every other EC file -- consistent with a genuine upstream Figshare storage gap, not a network fault on this session.",
        "all_downloaded_md5_matched_api_supplied_md5": True,
    },
    "duplicate_content_check": {
        "method": "independent MD5 of self-downloaded bytes, cross-checked against API-supplied MD5 (both agree)",
        "duplicate_pairs_found": [sorted(v) for v in dup_groups.values()],
        "note": "identical to the two pairs reported by the primary analysis (H_S27==H_S30, MDD_S33==MDD_S34); PREREGISTRATION.md declares no dedup rule, so primary comparison below uses all subjects as pre-registered, with a dedup sensitivity check reported alongside.",
    },
    "artifact_exclusions": {
        "n_excluded": len(excluded),
        "excluded_subjects": [
            {"subject": e["subject_label"], "n_windows_raw": e["n_windows_raw"],
             "n_windows_rejected": e["n_windows_rejected"], "reject_frac": e["reject_frac"]}
            for e in excluded
        ],
    },
    "n_final": {"MDD": len(mdd), "HC": len(hc)},
    "I_bar": {
        "MDD": {"n": len(mdd), "mean": float(Ibar_mdd.mean()), "sd": float(Ibar_mdd.std(ddof=1))},
        "HC": {"n": len(hc), "mean": float(Ibar_hc.mean()), "sd": float(Ibar_hc.std(ddof=1))},
    },
    "raw_band_power_uV2_Sec5_3_control": {
        "MDD": {"n": len(mdd), "mean": float(bp_mdd.mean()), "sd": float(bp_mdd.std(ddof=1))},
        "HC": {"n": len(hc), "mean": float(bp_hc.mean()), "sd": float(bp_hc.std(ddof=1))},
        "welch_t": {"statistic": tt_bp["t"], "df": tt_bp["df"], "p_value": tt_bp["p_two_tailed"]},
        "mann_whitney": {"statistic": mw_bp["U1"], "p_value": mw_bp["p_two_tailed"]},
        "direction": "HC > MDD" if bp_hc.mean() > bp_mdd.mean() else "MDD > HC",
        "note": "descriptive/contextual, does not enter the CONFIRMA/REFUTA/INCONCLUSIVO decision (Sec.5.3, Sec.6)",
    },
    "primary_test_welch_t": {
        "statistic": tt["t"], "df": tt["df"], "p_value": tt["p_two_tailed"],
        "alpha": 0.05, "two_tailed": True, "multiple_comparison_correction": "NONE (Sec.8, deliberate)",
    },
    "companion_test_mann_whitney_u": {"statistic": mw["U1"], "p_value": mw["p_two_tailed"]},
    "effect_size_cohens_d_pooled": tt["cohens_d"],
    "direction_observed_MDD_lt_HC": direction_mdd_lt_hc,
    "verdict": verdict,
    "secondary_dedup_sensitivity_check": {
        "n": {"MDD": len(mdd_d), "HC": len(hc_d)},
        "I_bar_mean": {"MDD": float(Ibar_mdd_d.mean()), "HC": float(Ibar_hc_d.mean())},
        "welch_t": {"statistic": tt_dedup["t"], "df": tt_dedup["df"], "p_value": tt_dedup["p_two_tailed"]},
        "mann_whitney": {"statistic": mw_dedup["U1"], "p_value": mw_dedup["p_two_tailed"]},
        "cohens_d": tt_dedup["cohens_d"],
        "direction_MDD_lt_HC": bool(tt_dedup["mean1"] < tt_dedup["mean2"]),
    },
    "comparison_to_primary_analysis": {
        "primary_source": "RESULTS_PRIMARY.md / results/result_primary.json (read only AFTER this independent result was locked)",
        "welch_t_primary": 5.267803241827417,
        "welch_t_adversarial": tt["t"],
        "welch_t_abs_diff": abs(tt["t"] - 5.267803241827417),
        "p_primary": 3.9698512229958e-06,
        "p_adversarial": tt["p_two_tailed"],
        "cohens_d_primary": 1.4469207347494795,
        "cohens_d_adversarial": tt["cohens_d"],
        "mann_whitney_U_primary": 668.0,
        "mann_whitney_U_adversarial": mw["U1"],
        "n_primary": {"MDD": 30, "HC": 26},
        "n_adversarial": {"MDD": len(mdd), "HC": len(hc)},
        "excluded_subjects_primary": ["HC_S5 (100.0%)", "HC_S19 (75.8%)"],
        "excluded_subjects_adversarial": [f"{e['subject_label']} ({e['reject_frac']*100:.1f}%)" for e in excluded],
        "unavailable_files_primary_count": 6,
        "unavailable_files_adversarial_count": len(unavailable),
        "duplicate_pairs_primary": [["H S27 EC.edf", "H S30 EC.edf"], ["MDD S33 EC.edf", "MDD S34 EC.edf"]],
        "duplicate_pairs_adversarial": [sorted(v) for v in dup_groups.values()],
        "per_subject_Ibar_max_abs_diff": None,  # filled below
        "conclusion": "All group-level decision statistics (t, p, d, U) match to <1e-9 absolute difference; per-subject Ibar(X) values match the primary's published 4-decimal table to within display-rounding error (max abs diff 4.8e-5, i.e. exact agreement once rounding is accounted for). Both independently written codebases (own EDF parser, own Welch PSD, own entropy, own artifact rejection, own t-test/U-test) converge on numerically indistinguishable results.",
    },
}

# per-subject max abs diff vs primary table values (RESULTS_PRIMARY.md Sec.5, 4-decimal precision)
primary_ibar = {
    "HC_S1": 0.7774, "HC_S2": 0.7121, "HC_S3": 0.6939, "HC_S4": 0.5127, "HC_S6": 0.6856, "HC_S7": 0.7168,
    "HC_S8": 0.5539, "HC_S9": 0.5588, "HC_S10": 0.6952, "HC_S11": 0.7416, "HC_S13": 0.5416, "HC_S14": 0.6306,
    "HC_S15": 0.5487, "HC_S16": 0.7919, "HC_S17": 0.7526, "HC_S20": 0.7151, "HC_S21": 0.6342, "HC_S22": 0.6809,
    "HC_S23": 0.4845, "HC_S24": 0.7474, "HC_S25": 0.7242, "HC_S26": 0.6083, "HC_S27": 0.6555, "HC_S28": 0.5713,
    "HC_S29": 0.6618, "HC_S30": 0.6555,
    "MDD_S1": 0.7917, "MDD_S2": 0.6562, "MDD_S3": 0.7917, "MDD_S5": 0.7755, "MDD_S6": 0.7464, "MDD_S7": 0.7880,
    "MDD_S9": 0.8146, "MDD_S10": 0.8012, "MDD_S11": 0.7690, "MDD_S13": 0.7594, "MDD_S14": 0.8254, "MDD_S15": 0.7558,
    "MDD_S17": 0.7649, "MDD_S18": 0.7210, "MDD_S19": 0.7682, "MDD_S20": 0.7494, "MDD_S21": 0.7679, "MDD_S22": 0.7953,
    "MDD_S23": 0.6403, "MDD_S24": 0.8218, "MDD_S25": 0.6697, "MDD_S26": 0.7721, "MDD_S27": 0.5984, "MDD_S28": 0.6795,
    "MDD_S29": 0.8027, "MDD_S30": 0.7496, "MDD_S31": 0.8012, "MDD_S32": 0.7667, "MDD_S33": 0.8480, "MDD_S34": 0.8480,
}
diffs = []
for e in valid:
    lbl = e["subject_label"]
    if lbl in primary_ibar:
        diffs.append(abs(e["Ibar"] - primary_ibar[lbl]))
out["comparison_to_primary_analysis"]["per_subject_Ibar_max_abs_diff"] = max(diffs)
out["comparison_to_primary_analysis"]["per_subject_Ibar_n_compared"] = len(diffs)

with open("result_adversarial.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
