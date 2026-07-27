# Final Agent Execution Report

## What was divergent

- The repository had a strong narrative layer, but the active `M_c v1` code still used local defaults and hidden constants.
- The `1e-15 kg / 50 µm / 0.1 s` target had been treated too much like a single supported point.
- The comparison ranking was being read too strongly for a dataset that is not yet discriminating.
- Outputs had no enforced provenance chain.

## What was corrected

- Introduced a canonical frozen contract: `config/tamesis_mc_v1.yaml`
- Added lock-based fail-closed validation
- Bound the active model to the contract
- Added protocol ID and config hash to outputs
- Added provenance sidecars for generated artifacts
- Added automatic manifest generation
- Added a schema-expanded literature table
- Marked the old model ranking as `legacy_exploratory_ranking`
- Bound figure generation directly to the canonical contract

## Files analyzed

- `mc_model.py`
- `config.py`
- `environment_model.py`
- `compare_models.py`
- `analyze_target_1e15.py`
- `prioritize_targets.py`
- `run_predictions.py`
- `target_1e15_noise_budget.py`
- `target_1e15_sensitivity.py`
- `target_1e15_decision.py`
- `target_1e15_thermal_gate.py`
- `generate_figures.py`
- `build_manifest.py`
- `verify_artifacts.py`
- `validate_contract.py`
- `regenerate_all.py`
- `run_tests.py`
- `provenance.py`
- `workspace_paths.py`
- `data/*`
- `reports/*`

## Files created

- `config.py`
- `config/tamesis_mc_v1.schema.json`
- `config/tamesis_mc_v1.lock.json`
- `reports/PARAMETER_SOURCE_MAP_V1_0.md`
- `reports/V1_0_REPOSITORY_AUDIT.md`
- `reports/MODEL_CONTRACT_V1_0.md`
- `reports/CONTRACT_IMPLEMENTATION_CONSISTENCY.md`
- `reports/V1_0_REGENERATION_DIFF.md`
- `reports/TARGET_1E15_FEASIBILITY_AUDIT.md`
- `reports/ENVIRONMENT_MODEL_AUDIT.md`
- `reports/LITERATURE_DATA_AUDIT.md`
- `reports/STATISTICAL_ANALYSIS_PLAN_V1_0.md`
- `reports/V1_0_EXECUTABLE_FREEZE_REPORT.md`
- `data/artifact_manifest.json`
- `data/literature_points_v2.csv`

## Files modified

- `mc_model.py`
- `compare_models.py`
- `analyze_target_1e15.py`
- `prioritize_targets.py`
- `run_predictions.py`
- `target_1e15_noise_budget.py`
- `target_1e15_sensitivity.py`
- `target_1e15_decision.py`
- `target_1e15_thermal_gate.py`
- `generate_figures.py`
- `build_manifest.py`
- `verify_artifacts.py`
- `validate_contract.py`
- `regenerate_all.py`
- `run_tests.py`
- `README.md`
- `STATUS.md`
- `data/README.md`
- `reports/README.md`

## Results reproduced

- `M_c = 5.292674126388712e-16 kg`
- `tau_c = 2.176246482178091 s`
- `V(0.1 s) = 0.8487106863823988`
- `V(1 s) = 0.19390843688831894`
- `1e-15 kg / M_c = 1.8894040632770233`
- `12 tests passed`

## Results that changed

- No core physical result changed.
- Only metadata, provenance, and executable freeze structure changed.
- The old ranking is now explicitly exploratory.

## Causes of change

- Contract freeze
- Fail-closed validation
- Provenance sidecars
- Automatic manifest
- Schema-expanded literature table

## Artifacts classified as legacy

- Historical root folders moved to `90_LEGACY`
- Old ranking interpretation
- Rival-model hardcoded defaults in the comparison scaffold remain exploratory until formalized

## Test coverage

- positive contract validation: passed
- numerical regression tests: passed
- manifest regeneration: passed
- artifact verification: passed
- pytest: passed (`12 passed`)

## Negative tests executed

The executable freeze now rejects:

- config/version mismatch
- hash mismatch
- `M_c` drift
- `tau_c` drift
- exponent drift
- missing config
- missing lock

## Official commands

```powershell
python validate_contract.py
python run_predictions.py
python compare_models.py
python analyze_target_1e15.py
python target_1e15_noise_budget.py
python target_1e15_sensitivity.py
python target_1e15_decision.py
python target_1e15_thermal_gate.py
python prioritize_targets.py
python generate_figures.py
python build_manifest.py
python verify_artifacts.py
python -m pytest -q
```

## Remaining limitations

- CSL / GRW / DP are still scaffold-level, not publication-grade full implementations.
- The environmental model is still first-pass only.
- The literature table still needs a fully validated provenance schema for every row.
- The `1e-15 kg / 50 µm` geometry remains provisional.

## Confirmation

No adjustable refit was performed.
The executable freeze is now enforced by the contract loader and lock file.
