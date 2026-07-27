# Critical coverage gaps

Comando: `python -m coverage run --branch -m pytest -q; python -m coverage report -m`. Resultado: **12 passed**, cobertura total de linhas instrumentadas 83%, mas porcentagem não é prova.

| Área | Coberta pelos 12 testes? | Evidência/gap |
| --- | --- | --- |
| loader/schema | parcial | test_contract_freeze cobre mutações Mc/expoente/unidade; campos alpha/largura/ausência ainda sem teste pytest |
| cálculo independente Mc/tau | sim/parcial | test_contract_freeze + validate_contract; tau exato não tem teste dedicado |
| hash/protocol | sim | test_hash_is_deterministic e protocol ID |
| figuras/GIFs | não | audit_model_summary_independence + clean_reproduce |
| sidecars/manifesto/fail-closed | não | mutation audit manual executável |
| overrides | não | audit_fail_closed e audit_freeze |
| legado | não | audit_imports AST |
| linhas/branches críticos | não | config.py:39 non-finite guard; config.py:161-167 runtime override branches (manual audit covers entry point); config.py:248-251 resolved payload branches; mc_model.py:81-82 negative mass; mc_model.py:86-91 invalid time/environment; provenance.py:100-121 malformed/missing/stale chain; build_manifest.py:52-82 malformed/stale/invalid sidecars; verify_artifacts.py:31-65 all mutation branches; generate_figures.py:29-42 input-sidecar failure; all official entrypoint mains outside unit suite |

A lacuna principal para uma suíte futura é transformar as auditorias manuais em testes pytest parametrizados sem aumentar a superfície física do modelo.
