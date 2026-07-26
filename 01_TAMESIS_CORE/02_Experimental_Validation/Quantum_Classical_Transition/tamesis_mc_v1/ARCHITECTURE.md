# Architecture

## Root

The root stays small and executable:

- `mc_model.py`
- `environment_model.py`
- `run_predictions.py`
- `compare_models.py`
- `prioritize_targets.py`
- `analyze_target_1e15.py`
- `target_1e15_*.py`
- `test_*.py`
- `README.md`
- `STATUS.md`
- `workspace_paths.py`

## Data

`data/` contains generated tables and JSON outputs.

## Reports

`reports/` contains human-readable documentation, decision notes, and the
target dossiers.

## Why this layout

- code remains easy to execute from the workspace root;
- generated outputs stop cluttering the root;
- reports and raw outputs become visually distinct;
- the archive can still preserve the older lineage outside this folder.

## Stable rule

Never rewrite the historical archive to make the story prettier.
Only the `tamesis_mc_v1` layer should be curated as an operational workspace.
