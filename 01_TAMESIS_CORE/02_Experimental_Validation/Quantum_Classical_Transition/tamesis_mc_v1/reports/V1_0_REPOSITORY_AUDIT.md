# V1.0 Repository Audit — Tamesis M_c v1

## Scope

This audit covers the active module:

`01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1`

and the root-facing outputs mirrored for inspection.

## Relevant tree

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
- `config/tamesis_mc_v1.yaml`
- `data/`
- `reports/`

## Entry points

- `python run_predictions.py`
- `python compare_models.py`
- `python analyze_target_1e15.py`
- `python prioritize_targets.py`
- `python target_1e15_noise_budget.py`
- `python target_1e15_sensitivity.py`
- `python target_1e15_decision.py`
- `python target_1e15_thermal_gate.py`
- `python generate_figures.py`
- `python -m pytest -q`

## What is actually implemented

### Tamesis v1 core

- `M_c = m_P (a_0/a_P)^(1/8)`
- `a_0 = c H_0`
- `Gamma_T(M) = 0` for `M <= M_c`
- `Gamma_T(M) = tau_c^-1 (M/M_c)^2` for `M > M_c`
- `V(t) = exp(-(Gamma_T + Gamma_env)t)`

### Environmental first-pass layer

- gas collision rate
- scalar magnetic/current nuisance rate
- scalar blackbody nuisance rate

### Comparison scaffold

- Tamesis
- CSL
- GRW
- Diósi–Penrose
- environment baseline

## Main audit findings

1. The model is phenomenological and auditable, not yet a physical proof.
2. Separation dependence is absent in v1.0; only mass and time enter the Tamesis rate.
3. The `1e-15 kg` target is useful, but the `1e-15 kg / 50 µm / 0.1 s` combination is not yet a fully audited platform guarantee.
4. The historical ranking is exploratory only.
5. The observed literature table is not yet discriminating because all observed rows lie far below `M_c`.
6. The current environmental model is intentionally simplified and not publication-grade.

## Duplicate / conflicting items

- `M_c` appears in code, JSON outputs, reports, and status docs.
- `7e-13 Pa` appears as a scenario-specific first-pass pressure requirement, not a universal law.
- `4 K` appears as a conservative blackbody gate, not a universal temperature cutoff.
- The `1e-15 kg` target appears both as a source-supported upper mass and as a hypothesis-composed ideal target.
- The `50 µm` separation appears in one proposal-derived narrative, but the supporting source also contains a much smaller-separation regime for the upper mass edge.

## Code / output classification

- `mc_model.py`: model assumption / derived core
- `environment_model.py`: model assumption
- `compare_models.py`: exploratory scaffold
- `generate_figures.py`: illustrative only
- `data/*.json`: derived results
- `data/literature_points.csv`: mixed observed + planned table
- `reports/*.md`: audit / interpretation
- `reports/figures/*`: illustrative only

## Reproducibility notes

- Tests pass in the current workspace.
- Figures and loop animations are reproducible through `generate_figures.py`.
- The comparison ranking is not yet statistically identified from the available observed dataset.

## Current scientific status

The repository is now in the state:

> hypothesis phenomenologically organized, with a preliminary experimental target, but still without independent physical or statistical validation.

