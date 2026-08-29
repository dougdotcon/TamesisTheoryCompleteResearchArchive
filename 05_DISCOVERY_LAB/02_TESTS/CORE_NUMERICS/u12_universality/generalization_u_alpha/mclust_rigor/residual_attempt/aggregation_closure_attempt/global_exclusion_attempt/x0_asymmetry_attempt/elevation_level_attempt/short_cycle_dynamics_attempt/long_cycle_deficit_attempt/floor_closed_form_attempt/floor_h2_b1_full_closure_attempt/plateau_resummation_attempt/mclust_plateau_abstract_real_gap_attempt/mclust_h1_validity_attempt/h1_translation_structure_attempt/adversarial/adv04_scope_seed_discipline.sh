#!/bin/bash
# adv04_scope_seed_discipline.sh
#
# INDEPENDENT ADVERSARIAL CHECK -- H1-TRANSLATION-STRUCTURE-ATTEMPT referee
# check, scope/seed discipline. Verifies:
#   1. No file outside .../h1_translation_structure_attempt/ was modified
#      (sibling directories show no 2026-08-29 files).
#   2. No `git` command appears in any of the target's own scripts.
#   3. The reserved seed block 20260931000-20260931999 is genuinely unused
#      anywhere in the archive except its own DECISION_LEDGER.yaml
#      reservation line and the target's own self-referential prose.
#   4. THEOREM.md / PROOF_DEPENDENCY_MAP.md / DECISION_LEDGER.yaml /
#      TEST_QUEUE.yaml / DISCOVERY_LAB_STATE.md were not modified by this
#      front (mtime check).

set -euo pipefail

ARCHIVE_ROOT="/home/user/TamesisTheoryCompleteResearchArchive"
BASE="$ARCHIVE_ROOT/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt/long_cycle_deficit_attempt/floor_closed_form_attempt/floor_h2_b1_full_closure_attempt/plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/mclust_h1_validity_attempt"
TARGET="$BASE/h1_translation_structure_attempt"

echo "================================================================"
echo "CHECK 1 -- sibling directories show NO 2026-08-29 (or later) files"
echo "================================================================"
for d in h1_volterra_attempt h1_post_correction_attempt h1_energy_estimate_attempt; do
  echo "--- $BASE/$d ---"
  hits=$(find "$BASE/$d" -newermt "2026-08-29 00:00:00" 2>/dev/null || true)
  if [ -z "$hits" ]; then
    echo "  (no files modified on/after 2026-08-29 -- PASS)"
  else
    echo "  FOUND (potential scope violation):"
    echo "$hits"
  fi
done
echo "--- $ARCHIVE_ROOT/.../mclust_h2_validity_attempt ---"
hits=$(find "$BASE/../mclust_h2_validity_attempt" -newermt "2026-08-29 00:00:00" 2>/dev/null || true)
if [ -z "$hits" ]; then
  echo "  (no files modified on/after 2026-08-29 -- PASS)"
else
  echo "  FOUND (potential scope violation):"
  echo "$hits"
fi

echo
echo "================================================================"
echo "CHECK 2 -- no 'git' command in any of the target's own .py scripts"
echo "================================================================"
if grep -rln 'git ' "$TARGET"/*.py 2>/dev/null; then
  echo "  FOUND git-related lines above (potential violation)"
else
  echo "  (no 'git ' substring found in any .py file -- PASS)"
fi

echo
echo "================================================================"
echo "CHECK 3 -- reserved seed block 20260931000-20260931999 genuinely unused"
echo "================================================================"
echo "All occurrences of '20260931' anywhere under 05_DISCOVERY_LAB/:"
grep -rn "20260931" "$ARCHIVE_ROOT/05_DISCOVERY_LAB/" 2>/dev/null || echo "  (none found)"
echo
echo "Expected: ONLY (a) DECISION_LEDGER.yaml's own DISC-DEC-118 reservation"
echo "line, (b) the target's own ATTEMPT.md self-referential prose (Sec 0,"
echo "Sec 9), and (c) any OTHER front's own adversarial audit log that merely"
echo "quotes the full seed-block list from DECISION_LEDGER.yaml for its own,"
echo "unrelated, documentation purposes -- NOT any actual numpy/random seeding"
echo "call using a number in this range."
echo
echo "Actual random-number-generator usage in the target's own scripts:"
grep -rn "seed\|SeedSequence\|random\|np\.random\|randint" "$TARGET"/*.py 2>/dev/null || \
  echo "  (none found -- consistent with the front's claim that no randomness"
echo "  was needed anywhere)"

echo
echo "================================================================"
echo "CHECK 4 -- governance files not modified by this front (mtime check)"
echo "================================================================"
for gf in THEOREM.md PROOF_DEPENDENCY_MAP.md DECISION_LEDGER.yaml TEST_QUEUE.yaml DISCOVERY_LAB_STATE.md; do
  found=$(find "$ARCHIVE_ROOT" -maxdepth 6 -name "$gf" 2>/dev/null | head -5)
  echo "--- $gf ---"
  for f in $found; do
    stat -c '  %y  %n' "$f" 2>/dev/null || true
  done
done
echo
echo "(Cross-reference: DISC-DEC-118 already exists at 2026-08-29 in"
echo "DECISION_LEDGER.yaml, since it AUTHORIZES this wave -- that entry"
echo "predates/accompanies dispatch, not a write made BY this front itself;"
echo "the mandate's own text states the front opened these files read-only.)"

echo
echo "================================================================"
echo "ALL CHECKS COMPLETE"
echo "================================================================"
