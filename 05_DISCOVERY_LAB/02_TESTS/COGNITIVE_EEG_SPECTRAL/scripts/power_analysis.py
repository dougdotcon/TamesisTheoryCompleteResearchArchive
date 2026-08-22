"""
A priori statistical power analysis for DISC-COGNITIVE-EEG-SPECTRAL-001,
operationalization stage (DISC-DEC-025). Does NOT touch any real EEG data --
uses only the sample sizes verified in SURVEY.md / TEST_QUEUE.yaml and a
plausible range of standardized effect sizes (Cohen's d), consistent with
Cohen, J. (1988). "Statistical Power Analysis for the Behavioral Sciences"
(2nd ed.), Lawrence Erlbaum Associates -- the standard reference for the
d=0.2/0.5/0.8 small/medium/large convention used throughout.

Method: statsmodels.stats.power (TTestIndPower for the independent-groups
Mumtaz MDD-vs-HC design, TTestPower for the paired within-subject DASPS
design), which implements the noncentral-t-distribution exact power
calculation for Student's t-test (Cohen 1988, ch. 2 and ch. 3).
"""
import numpy as np
from statsmodels.stats.power import TTestIndPower, TTestPower

ALPHA_TWO_SIDED = 0.05
EFFECT_SIZES = [0.2, 0.3, 0.5, 0.8]  # small, small-medium, medium, large (Cohen 1988)

print("=" * 78)
print("MUMTAZ (independent two-sample design): N_MDD=34, N_HC=30")
print("Two-sided alpha =", ALPHA_TWO_SIDED)
print("=" * 78)
ind_power = TTestIndPower()
n1, n2 = 34, 30
# statsmodels' solve_power for TTestIndPower takes a single nobs1 and a
# ratio nobs2/nobs1 for unequal group sizes.
ratio = n2 / n1
for d in EFFECT_SIZES:
    power = ind_power.power(effect_size=d, nobs1=n1, ratio=ratio, alpha=ALPHA_TWO_SIDED, alternative="two-sided")
    print(f"  Cohen's d = {d:0.2f}  ->  power = {power:0.4f}")

print()
# Also report minimum detectable effect size for 80% power at this fixed N
d_needed = ind_power.solve_power(effect_size=None, nobs1=n1, ratio=ratio, alpha=ALPHA_TWO_SIDED, power=0.80, alternative="two-sided")
print(f"Minimum detectable Cohen's d for 80% power at N=(34,30): d = {d_needed:0.4f}")

print()
print("=" * 78)
print("DASPS (paired within-subject design, one obs pair per subject): N=23")
print("Two-sided alpha =", ALPHA_TWO_SIDED)
print("=" * 78)
paired_power = TTestPower()
n = 23
for d in EFFECT_SIZES:
    power = paired_power.power(effect_size=d, nobs=n, alpha=ALPHA_TWO_SIDED, alternative="two-sided")
    print(f"  Cohen's d (of the paired difference) = {d:0.2f}  ->  power = {power:0.4f}")

print()
d_needed_paired = paired_power.solve_power(effect_size=None, nobs=n, alpha=ALPHA_TWO_SIDED, power=0.80, alternative="two-sided")
print(f"Minimum detectable Cohen's d for 80% power at N=23 (paired): d = {d_needed_paired:0.4f}")

print()
print("=" * 78)
print("Context: what effect size does the closest real precedent in this")
print("archive give for the SAME statistical family (entropy/complexity of")
print("physiological signal, pre/post comparison)?")
print("=" * 78)
print("""
02_TESTS/TRI_RG/permutation_entropy/RESULTS_SUMMARY.md (DISC-TRI-RG-001,
VitalDB anesthesia induction, EEG channel BIS/EEG1_WAV, N=1 subject/segment
pair per domain, so not directly N-comparable) reports PRE/POST deltas of
order 1e-3 on PCI (~13.88 scale) and MCI (~0.15-0.26 scale) with p in
[0.97, 0.995] -- i.e. statistically indistinguishable from the IAAFT null
in that single-subject/single-domain application. That test is a within-
subject state-transition design, not a between-subject diagnostic-
classification design, so its N and design do not transfer directly to a
power number here -- it is reported only as prior/contextual honesty about
what this statistical family has produced in this lab so far (a negative
result), not as an input to the power calculation itself.
""")
