# Status de auditoria — Tamesis M_c v1.0

## Referência numérica

Esta versão fixa, para o protocolo v1.0:

\[
M_c=5.2926741264\times10^{-16}\;\mathrm{kg}
\]

obtido de \(H_0=70\) km s⁻¹ Mpc⁻¹ e da hipótese de raiz oitava. O valor não é
uma constante medida nem uma derivação concluída.

## Conflitos legados encontrados

- `massa_critica/simulations/constants.py` usa a mesma escala de
  \(5.29\times10^{-16}\) kg, mas mistura estados “derivado”, “calibrado” e
  “hipótese”.
- `03_Axiomatic_Closure/Killer_Prediction/interference_sim.py` usa
  `M_c = 2.2e-14 kg`, sem explicar a mudança de duas ordens de magnitude e sem
  separar parâmetro de visualização de previsão física.
- Os gráficos e códigos antigos usam curvas ajustadas para ilustração; eles não
  são dados experimentais e não devem ser usados para estimar a evidência da
  v1.0.

## Camada de comparacao adicionada

- `compare_models.py` executa a comparacao com CSL, GRW, DP e um baseline
  ambiental com taxa de nuisance por familia. O ranking resultante agora deve
  ser tratado como `legacy_exploratory_ranking`.
- `reports/preregistration.md` fixa o plano estatistico antes da inferencia.
- `data/literature_points.csv` separa pontos observados de alvos planejados.
- `reports/BOHR_LEVEL_GAP.md` registra a distancia entre a fronteira experimental atual
  e o teste decisivo em torno de M_c.
- `reports/EXPERIMENTAL_FRONTIER_SOURCES.md` registra as fontes externas usadas para
  alimentar a tabela experimental.
- `reports/NANODIAMOND_TARGET_DOSSIER.md` registra o primeiro alvo encontrado que cruza
  diretamente o M_c do Tamesis.
- `prioritize_targets.py` e `data/target_priority_report.json` ranqueiam alvos
  planejados por proximidade/discriminacao em relacao a M_c.
- `reports/NEXT_EXPERIMENT_STRATEGY.md` define o alvo experimental mais promissor:
  superposicao espacial de nanodiamante em torno de `1e-15 kg`.
- `environment_model.py`, `analyze_target_1e15.py` e
  `data/target_1e15_analysis.json` iniciam a comparacao dura contra ambiente para o
  alvo `1e-15 kg`.
- `reports/TARGET_1E15_RESULT.md` resume o primeiro resultado: para gas residual ficar
  abaixo de 10% do efeito Tamesis no alvo `1e-15 kg`, a pressao precisa ser
  aproximadamente menor que `7e-13 Pa`.
- `target_1e15_noise_budget.py` e `reports/TARGET_1E15_NOISE_BUDGET.md` traduzem as
  tolerancias de gradiente/posicao em um orçamento de ruido normalizado.
- `target_1e15_decision.py` e `reports/TARGET_1E15_DECISION.md` fecham a primeira
  decisao operacional para o alvo `1e-15 kg`.
- `target_1e15_thermal_gate.py` e `reports/TARGET_1E15_THERMAL_GATE.md` fixam a
  barreira termica conservadora em torno de `4 K`.

## Limite atual

A comparacao ainda esta limitada ao que o archive traz em forma tabular. Para
virar analise forte de verdade, ainda falta uma tabela bruta completa com:
massa, separacao, tempo, visibilidade, pressao, temperatura, geometria e
incerteza por experimento.

## Regra de versionamento

Nenhum parâmetro de \(M_c\), \(\alpha\), \(\tau_c\) ou largura de transição
pode ser alterado depois de observar um conjunto de dados e ainda ser chamado
de teste v1.0. Qualquer alteração gera v1.1, com justificativa e novo protocolo.
