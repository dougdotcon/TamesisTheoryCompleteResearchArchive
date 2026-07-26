# Final Agent Execution Report

## Files analyzed

- `mc_model.py`
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
- `workspace_paths.py`
- `test_mc_model.py`
- `test_environment_model.py`
- `README.md`
- `STATUS.md`
- `data/*`
- `reports/*`

## Files created

- `config/tamesis_mc_v1.yaml`
- `reports/V1_0_REPOSITORY_AUDIT.md`
- `reports/MODEL_CONTRACT_V1_0.md`
- `reports/TARGET_1E15_FEASIBILITY_AUDIT.md`
- `reports/ENVIRONMENT_MODEL_AUDIT.md`
- `reports/LITERATURE_DATA_AUDIT.md`
- `reports/STATISTICAL_ANALYSIS_PLAN_V1_0.md`
- `data/artifact_manifest.json`
- `data/literature_points_v2.csv`

## Files modified

- `compare_models.py`
- `README.md`
- `README_PTBR.md`
- `00_HOME/README.md`
- `reports/README.md`
- `reports/VISUAL_ANALYSIS.md`

## Conflicts found

- `50 µm` vs source-supported `~1 nm` upper-edge geometry
- ranking output was exploratory, not identifiable
- `7e-13 Pa` is scenario-specific, not universal
- `4 K` is conservative, not universal
- observed literature data remain below `M_c`

## Reproduced results

- `M_c = 5.292674126388712e-16 kg`
- `tau_c = 2.176246482178091 s`
- `V(0.1 s) ≈ 0.8487` for `1e-15 kg`
- `V(1 s) ≈ 0.1939` for `1e-15 kg`
- `6 tests passed`
- figures and GIFs regenerated successfully

## Not yet reproduced as hard science

- independent validation of the physical threshold
- identifiable model ranking
- publication-grade CSL / GRW / DP implementations
- full environmental channel decomposition

## Bugs / issues corrected

- ranking renamed to `legacy_exploratory_ranking`
- visible root outputs created for easier inspection
- figure generation made reproducible and looped

## Status summary

- `M_c`: reproduced numerically
- `50 µm` scenario: provisional / not yet fully source-supported
- pressure limit: scenario-specific
- thermal gate: conservative
- ranking: legacy exploratory only

## Repro command

```powershell
python run_predictions.py
python compare_models.py
python analyze_target_1e15.py
python target_1e15_noise_budget.py
python target_1e15_sensitivity.py
python target_1e15_decision.py
python target_1e15_thermal_gate.py
python generate_figures.py
python -m pytest -q
```

## Bottom line

The project is now organized enough to audit, but not yet ready to claim a Bohr-level discovery.
