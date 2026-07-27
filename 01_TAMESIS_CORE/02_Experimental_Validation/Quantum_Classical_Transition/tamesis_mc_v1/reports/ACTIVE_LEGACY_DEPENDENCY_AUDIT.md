# Active versus legacy dependency audit

Comando: `python audit_imports.py`, usando `ast` e resolução de módulos locais; não é busca textual. Foram visitados **19 módulos** a partir dos entry points oficiais e encontrados **0 edges para 90_LEGACY/legado**.

| Fonte | Imports locais |
| --- | --- |
| analyze_target_1e15.py | compare_models.py, config.py, environment_model.py, mc_model.py, provenance.py, workspace_paths.py |
| build_manifest.py | config.py |
| compare_models.py | config.py, mc_model.py, provenance.py, workspace_paths.py |
| config.py | — |
| environment_model.py | — |
| generate_figures.py | config.py, provenance.py |
| mc_model.py | config.py |
| prioritize_targets.py | config.py, mc_model.py, provenance.py, workspace_paths.py |
| provenance.py | config.py |
| resolve_contract.py | config.py, provenance.py, workspace_paths.py |
| run_predictions.py | config.py, mc_model.py, provenance.py, workspace_paths.py |
| target_1e15_decision.py | analyze_target_1e15.py, config.py, mc_model.py, provenance.py, target_1e15_noise_budget.py, workspace_paths.py |
| target_1e15_noise_budget.py | analyze_target_1e15.py, config.py, mc_model.py, provenance.py, workspace_paths.py |
| target_1e15_sensitivity.py | analyze_target_1e15.py, config.py, mc_model.py, provenance.py, workspace_paths.py |
| target_1e15_thermal_gate.py | analyze_target_1e15.py, config.py, mc_model.py, provenance.py, workspace_paths.py |
| validate_contract.py | config.py, mc_model.py |
| validate_environment.py | config.py |
| verify_artifacts.py | build_manifest.py, config.py |
| workspace_paths.py | — |

Resultado: nenhum entry point ativo importa diretamente ou indiretamente `90_LEGACY`. O legado permanece no arquivo histórico e na busca estrutural como `expected_legacy`.
