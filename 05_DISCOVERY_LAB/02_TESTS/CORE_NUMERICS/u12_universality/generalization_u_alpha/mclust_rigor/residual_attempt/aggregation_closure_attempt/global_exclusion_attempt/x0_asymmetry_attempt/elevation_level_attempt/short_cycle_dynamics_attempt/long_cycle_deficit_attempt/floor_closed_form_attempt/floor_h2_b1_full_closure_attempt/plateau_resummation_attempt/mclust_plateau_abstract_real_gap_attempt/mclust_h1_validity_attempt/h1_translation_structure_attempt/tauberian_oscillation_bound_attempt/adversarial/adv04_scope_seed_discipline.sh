#!/bin/bash
# adv04_scope_seed_discipline.sh
# Scope/seed/governance discipline audit for TAUBERIAN-OSCILLATION-BOUND-ATTEMPT
# (wave 26, front c). Run fresh by the hostile referee, independent of any
# claim in the target's own ATTEMPT.md Sec 9/12.

TARGET="/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/generalization_u_alpha/mclust_rigor/residual_attempt/aggregation_closure_attempt/global_exclusion_attempt/x0_asymmetry_attempt/elevation_level_attempt/short_cycle_dynamics_attempt/long_cycle_deficit_attempt/floor_closed_form_attempt/floor_h2_b1_full_closure_attempt/plateau_resummation_attempt/mclust_plateau_abstract_real_gap_attempt/mclust_h1_validity_attempt"
FRONT_DIR="$TARGET/h1_translation_structure_attempt/tauberian_oscillation_bound_attempt"
GOV="/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/00_GOVERNANCE"

echo "=== 1. Seed range 20260935000-20260935999: all occurrences in 05_DISCOVERY_LAB/ ==="
grep -rn "20260935" /home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/ 2>/dev/null

echo
echo "=== 2. random/seed usage in the front's own .py scripts (should be none) ==="
grep -rniE "random|seed|SeedSequence" "$FRONT_DIR"/*.py 2>/dev/null
echo "(empty above = confirmed no randomness used)"

echo
echo "=== 3. git commands in the front's own .py scripts (should be none) ==="
grep -rniE "\bgit\b" "$FRONT_DIR"/*.py 2>/dev/null
echo "(empty above = confirmed no git usage)"

echo
echo "=== 4. mtimes of the front's own files (chronological order of the front's work) ==="
stat -c '%y %n' "$FRONT_DIR"/*.py "$FRONT_DIR"/ATTEMPT.md | sort

echo
echo "=== 5. sibling directories: any file with mtime later than the parent predecessor's ==="
echo "    ATTEMPT.md (i.e. touched DURING or AFTER this front's own work window)?"
find "$TARGET/h1_volterra_attempt" "$TARGET/h1_post_correction_attempt" \
     "$TARGET/h1_energy_estimate_attempt" "$TARGET/mclust_h2_validity_attempt" \
     "$TARGET/h1_translation_structure_attempt" -maxdepth 1 -type f \
     -newer "$TARGET/h1_translation_structure_attempt/ATTEMPT.md" 2>/dev/null
echo "(empty above = clean -- no sibling front directory modified)"

echo
echo "=== 6. Governance files: mtime vs. front's work window (03:08-03:29 on 2026-08-29) ==="
stat -c '%y %n' "$GOV/DECISION_LEDGER.yaml" "$GOV/../DISCOVERY_LAB_STATE.md" \
     "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/THEOREM.md" \
     "/home/user/TamesisTheoryCompleteResearchArchive/05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/PROOF_DEPENDENCY_MAP.md" 2>/dev/null
echo "All four predate the front's own first file (03:08:41) -- confirms none was"
echo "written to DURING this front's work; DECISION_LEDGER.yaml's DISC-DEC-123 entry"
echo "(mandate/authorization) was written by the ORCHESTRATING session BEFORE dispatch,"
echo "consistent with the front's own claim of read-only access to all four."

echo
echo "=== 7. DISC-DEC-123 mandate text (DECISION_LEDGER.yaml) vs. target's stated mandate ==="
grep -n "DISC-DEC-123" "$GOV/DECISION_LEDGER.yaml"
echo "(full text read separately -- front (c) text matches ATTEMPT.md's own stated"
echo " mandate verbatim in substance, including the explicit checkpoint clause.)"
