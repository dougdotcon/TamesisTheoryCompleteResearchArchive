# Fail-closed audit

Comando: `python audit_fail_closed.py`. Todos os casos abaixo terminaram com exit code 1, em cópias temporárias; o YAML oficial não foi alterado.

| Caso | Resultado | Evidência |
| --- | --- | --- |
| configuration_missing | exit 1 | ers\CLIENTE\AppData\Local\Temp\tamesis-fail-closed-aex3h76a\missing\01_TAMESIS_CORE\02_Experimental_Validation\Quantum_Classical_Transition\tamesis_mc_v1\config\tamesis_mc_v1.yaml  |
| configuration_invalid | exit 1 | onfig.py", line 219, in _validate_contract     raise ContractError("configuration hash does not match lock file") config.ContractError: configuration hash does not match lock file  |
| cli_override | exit 1 | ContractError(f"v1.0 entry points accept no CLI arguments or overrides: {argv!r}") config.ContractError: v1.0 entry points accept no CLI arguments or overrides: ['--M_c', '1e-15']  |
| environment_override | exit 1 | raise ContractError(f"v1.0 structural environment overrides are forbidden: {present}") config.ContractError: v1.0 structural environment overrides are forbidden: ['TAMESIS_MC_KG']  |
| sidecar_missing | exit 1 | ar for required input: {path}") RuntimeError: missing provenance sidecar for required input: C:\Users\CLIENTE\AppData\Local\Temp\tamesis-fail-closed-aex3h76a\sidecar\artifact.json  |
| manifest_stale | exit 1 | endence.py - unlisted artifact: clean_reproduce.py - unlisted artifact: data/clean_reproducibility_evidence.json - unlisted artifact: data/model_summary_independence_evidence.json  |

A configuração inválida falha antes de gerar resultado oficial. Sidecar ausente, manifesto stale e overrides também são recusados. A atomicidade de escritas pós-cálculo ainda é uma lacuna para falhas de I/O tardias.
