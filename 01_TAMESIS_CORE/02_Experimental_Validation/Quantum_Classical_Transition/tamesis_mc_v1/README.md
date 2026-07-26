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

## Execução

```powershell
python run_predictions.py
python -m pytest -q
```
