# Parameter Source Map v1.0

| Arquivo | Linha/função | Parâmetro | Valor | Uso | Status | Ação |
| ------- | ------------ | --------: | ----: | --- | ------ | ---- |
| `config/tamesis_mc_v1.yaml` | root | `version` | `1.0` | identidade do contrato | canonical | manter |
| `config/tamesis_mc_v1.yaml` | `constants.H0` | `H_0` | `70 km s^-1 Mpc^-1` | entrada cosmológica | canonical | manter |
| `config/tamesis_mc_v1.yaml` | `constants.G` | `G` | `6.67430e-11` | constante fundamental | canonical | manter |
| `config/tamesis_mc_v1.yaml` | `constants.hbar` | `ħ` | `1.054571817e-34` | constante fundamental | canonical | manter |
| `config/tamesis_mc_v1.yaml` | `structural_parameters.phase_space_root` | raiz oitava | `8` | estrutura v1.0 | canonical | congelar |
| `config/tamesis_mc_v1.yaml` | `structural_parameters.exponent` | expoente | `2.0` | taxa acima do limiar | canonical | congelar |
| `config/tamesis_mc_v1.yaml` | `structural_parameters.alpha` | `alpha` | `null` | ausente na v1.0 | canonical | manter ausente |
| `config/tamesis_mc_v1.yaml` | `structural_parameters.tau_c` | `tau_c` | `2.176246482178091 s` | escala temporal congelada | canonical | congelar |
| `config/tamesis_mc_v1.yaml` | `structural_parameters.transition_width` | largura | `null` | ausente na v1.0 | canonical | manter ausente |
| `mc_model.py` | `compute_mc_from_contract` | `M_c` | derivado | cálculo independente | duplicate_consistent | manter |
| `mc_model.py` | `McModel.__post_init__` | `M_c`, `tau_c` | validado | fail-closed | duplicate_consistent | manter |
| `mc_model.py` | `McModel.intrinsic_rate` | `M_c`, expoente | contrato | taxa intrínseca | duplicate_consistent | manter |
| `compare_models.py` | `predict_coherence_probability` | `lambda_csl` | `1e-16` | parâmetro rival CSL | legacy | mover para config rival se necessário |
| `compare_models.py` | `predict_coherence_probability` | `r_c` | `1e-7` | parâmetro rival CSL | legacy | mover para config rival se necessário |
| `compare_models.py` | `predict_coherence_probability` | `lambda_grw` | `1e-16` | parâmetro rival GRW | legacy | mover para config rival se necessário |
| `compare_models.py` | `predict_coherence_probability` | `a` | `1e-7` | parâmetro rival GRW | legacy | mover para config rival se necessário |
| `compare_models.py` | `predict_coherence_probability` | `DP` | fórmula local | aproximação exploratória | legacy | substituir por contrato rival formal |
| `analyze_target_1e15.py` | `mass/time` | alvo `1e-15 kg` | `50 µm, 0.1 s` | triagem experimental | duplicate_conflicting | separar de alvo fisicamente suportado |
| `reports/target_1e15_constraints.md` | Source 1 | `1e-15 kg / 50 µm / 0.1 s` | extraído do resumo | narrativa de alvo | duplicate_conflicting | tratar como hipótese idealizada |
| `reports/target_1e15_constraints.md` | Source 2 | `1e-15 kg / O(1 nm)` | extremo superior da proposta de 2026 | rota suportada pela fonte | duplicate_consistent | separar do alvo idealizado |
| `STATUS.md` | conflict note | `2.2e-14 kg` | legado | valor antigo conflitante | legacy | preservar como legado |
| `reports/MODEL_CONTRACT_V1_0.md` | contract | `M_c` | `5.292674126388712e-16 kg` | valor congelado | canonical | manter |
| `reports/MODEL_CONTRACT_V1_0.md` | contract | `tau_c` | `2.176246482178091 s` | valor congelado | canonical | manter |
| `run_predictions.py` | output row | `M/M_c` | valores fixos | tabela de previsão | duplicate_consistent | manter |
| `generate_figures.py` | plots | `M_c`, `1e-15 kg`, `4 K`, `7e-13 Pa` | visualização | visualization_only | manter |

## Summary

- canonical: contract fields in `config/tamesis_mc_v1.yaml`
- duplicate_consistent: contract-consistent derivations and outputs
- duplicate_conflicting: the `1e-15 kg / 50 µm` target is not yet fully source-supported as a single platform triple
- legacy: old rival defaults or historical conflicting values
- visualization_only: plot annotations and loop labels

