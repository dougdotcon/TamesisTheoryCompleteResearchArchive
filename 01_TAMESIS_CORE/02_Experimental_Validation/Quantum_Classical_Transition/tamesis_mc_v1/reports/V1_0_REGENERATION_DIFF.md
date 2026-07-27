# V1.0 Regeneration Diff

| Artefato | Resultado anterior | Resultado canônico | Diferença | Causa | Status |
| -------- | -----------------: | -----------------: | --------: | ----- | ------ |
| `model_summary.json` | `Mc_kg = 5.292674126388712e-16` | mesmo valor | 0 | sem mudança numérica | unchanged |
| `predictions.csv` | sem `protocol_id` | com `protocol_id` | metadata | freeze executável | superseded_metadata |
| `comparison_report.json` | `ranking` | `legacy_exploratory_ranking` | nomenclatura | evitar leitura científica indevida | superseded_metadata |
| `target_1e15_analysis.json` | sem `protocol_id` | com `protocol_id` | metadata | provenance | superseded_metadata |
| `target_1e15_noise_budget.json` | sem proveniência | com sidecar | provenance | freeze executável | superseded_metadata |
| `target_1e15_decision.json` | sem proveniência | com sidecar | provenance | freeze executável | superseded_metadata |
| `target_1e15_thermal_gate.json` | sem proveniência | com sidecar | provenance | freeze executável | superseded_metadata |
| `artifact_manifest.json` | manual | automático | pipeline | fail-closed | superseded_metadata |
| `figures/*.png` | sem sidecar | com sidecar | provenance | freeze executável | superseded_metadata |
| `figures/*.gif` | sem sidecar | com sidecar | provenance | freeze executável | superseded_metadata |

## Numerical note

No core physical result changed during the executable freeze:

- `M_c` stayed the same
- `tau_c` stayed the same
- `V(0.1 s)` stayed the same
- `V(1 s)` stayed the same

What changed was traceability, not the model's numerical core.

