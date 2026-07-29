# Auditoria — Neural-LMC

**Status:** needs_data  
**Classificação:** benchmark de aprendizado de máquina exploratório (S1/E)

## Veredicto

A ativação saturante pode reduzir explosão numérica em uma tarefa caótica, mas cinco sementes e um único atrator não demonstram transferência de um princípio físico. A redução de 77,5% precisa de distribuição de resultados, seleção de hiperparâmetros e controles equivalentes.

## Próximo teste

Pré-registrar arquitetura e métricas, repetir em Lorenz com horizontes variados e em outros sistemas caóticos, incluir ReLU/tanh/normalização e reportar média, dispersão e desempenho fora da amostra.

## Fontes

- [Lorenz, *Deterministic Nonperiodic Flow*](https://doi.org/10.1175/1520-0469%281963%29020%3C0130%3ADNF%3E2.0.CO%3B2)
- [Kato — operator perturbations](https://link.springer.com/book/10.1007/978-3-642-66282-9)
