# Tamesis M_c v1

Camada operacional da hipótese de massa crítica `M_c`.

## Leitura rápida

- `mc_model.py` define o modelo central.
- `environment_model.py` estima o ruído ambiental de primeira passagem.
- `analyze_target_1e15.py` fecha o alvo principal de `1e-15 kg`.
- `compare_models.py` compara Tamesis com CSL, GRW e Diósi-Penrose.
- `data/` contém saídas numéricas.
- `reports/` contém relatórios e decisões.

## Estado

Esta é uma versão fenomenológica e auditável.
Ela não prova a hipótese; ela a torna mensurável e falsificável.

A fase exclusivamente computacional está congelada desde 2026-07-26:

- `software_status: frozen_and_ready`
- `campaign_state: HARDWARE_QUALIFICATION_NOT_STARTED`
- `physical_evidence: false`
- `operational_status: PAUSED_PENDING_HARDWARE_AND_METROLOGY`

O próximo avanço exige metadados e calibrações de hardware reais. Não deve ser
criada uma v0.7 puramente computacional.

## Hipóteses fixas da v1

1. `M_c = m_P (a_0/a_P)^(1/8)` com `a_0 = cH_0`.
2. O expoente `1/8` é uma hipótese de fase-espaço.
3. `Gamma_T(M)=0` para `M<=M_c` e `Gamma_T(M)=tau_c^-1 (M/M_c)^2` para `M>M_c`.
4. O ruído ambiental entra como nuisance medido independentemente.

## Estrutura

- [Architecture](ARCHITECTURE.md)
- [Status](STATUS.md)
- [Reports](reports/README.md)
- [Data](data/README.md)
- [Project freeze](../../../../PROJECT_FREEZE.md)

## Execução

```powershell
python run_predictions.py
python -m pytest -q
```
