# Manifest behavior audit

Comando de construção: `python build_manifest.py`; verificação independente: `python verify_artifacts.py` (não reconstrói o manifesto).

Estados detectados em fixture controlada: `{"canonical_current": 1, "canonical_stale": 1, "illustrative_only": 1, "invalid": 1, "legacy": 1, "unknown_provenance": 1}`.

| Cenário | Resultado |
| --- | --- |
| artifact_edited | {"exit_code": 1, "message": "artifact verification failed:\n- manifest artifact hash mismatch: current.txt\n- canonical artifact is invalid: current.txt: artifact hash mismatch", "rejected": true} |
| artifact_removed | {"exit_code": 1, "message": "artifact verification failed:\n- manifest entry missing artifact: current.txt", "rejected": true} |
| manifest_edited | {"exit_code": 1, "message": "artifact verification failed:\n- manifest artifact hash mismatch: 90_LEGACY/legacy.txt", "rejected": true} |
| manual_unlisted_output | {"exit_code": 1, "message": "artifact verification failed:\n- unlisted artifact: manual_output.json", "rejected": true} |
| previous_version_unlisted_output | {"exit_code": 1, "message": "artifact verification failed:\n- unlisted artifact: official_previous_version.json", "rejected": true} |
| sidecar_removed | {"exit_code": 1, "message": "artifact verification failed:\n- sidecar removed: current.txt\n- canonical artifact is missing: current.txt: missing sidecar", "rejected": true} |
| sidecar_tampered | {"exit_code": 1, "message": "artifact verification failed:\n- manifest sidecar hash mismatch: current.txt\n- canonical artifact is invalid: current.txt: artifact hash mismatch", "rejected": true} |

No estado oficial final após a auditoria: 23 `canonical_current`, 0 `canonical_stale`, 0 `invalid`; arquivos sem sidecar permanecem `unknown_provenance` e não participam automaticamente da inferência.
