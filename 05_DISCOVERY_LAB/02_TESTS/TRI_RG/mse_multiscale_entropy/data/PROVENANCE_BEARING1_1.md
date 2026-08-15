# Proveniência — FEMTO/PRONOSTIA Bearing1_1 (dado real, domínio ENGENHARIA MECÂNICA)

## Fonte

- Dataset: FEMTO/PRONOSTIA (IEEE PHM 2012 Data Challenge), Nectoux et al. 2012.
- Host oficial: `https://phm-datasets.s3.amazonaws.com/NASA/10.+FEMTO+Bearing.zip`
  (~1,16GB, todos os rolamentos).
- Fonte efetivamente usada: mirror comunitário
  `https://github.com/wkzs111/phm-ieee-2012-data-challenge-dataset`,
  commit `577c77f1d8d284e2eadc8e17fe49d58907d7ad01`, via `git` sparse
  checkout + partial clone (`--filter=blob:none`) restrito a
  `Learning_set/Bearing1_1/`. Motivo: o zip oficial completo é ~1,16GB
  para todos os 17 rolamentos; o clone parcial baixou só os 2.803
  arquivos do rolamento `Bearing1_1` (~219MB), sem os demais rolamentos.
- Rolamento usado: `Bearing1_1` (conjunto `Learning_set`, run-to-failure
  completo). Confirmado: 2.803 arquivos `acc_00001.csv` .. `acc_02803.csv`,
  nenhum outro arquivo na pasta.
- Formato de cada `acc_XXXXX.csv`: 2.560 linhas, 6 colunas sem cabeçalho:
  `hora, minuto, segundo, contador, accel_horizontal_g, accel_vertical_g`.
  Intervalo entre amostras dentro de um burst ≈ 39,06 µs (25,6kHz),
  confirmado pela diferença entre valores sucessivos da coluna contador
  (39 unidades por amostra).
- Canal usado nesta análise: **acelerômetro horizontal** (coluna de
  índice 4, 0-based).
- Estrutura temporal real: 0,1s de gravação (2.560 amostras) a cada 10s
  (burst), portanto o teste NÃO é uma série contínua — há um gap real de
  ~9,9s de tempo de calendário entre o fim de um arquivo e o início do
  próximo.

## Concatenação dos bursts (decisão declarada)

Decisão tomada conforme instrução da tarefa: **(a)** os 2.803 bursts
foram concatenados em ordem cronológica de arquivo (`acc_00001.csv` →
`acc_02803.csv`), **ignorando o gap real de ~9,9s entre bursts** — a
série resultante é tratada como se fosse contígua por índice de
amostra.

- Total de amostras concatenadas: `2803 × 2560 = 7.175.680`.
- **Limitação declarada:** a estrutura de correlação real ao longo do
  tempo de CALENDÁRIO é truncada nos gaps de 10s (qualquer
  coarse-graining `tau` cujo bloco cruze uma fronteira de burst está, na
  prática, emendando amostras que são ~9,9s distantes uma da outra em
  tempo real, como se fossem consecutivas). A estrutura de correlação
  DENTRO de cada burst de 0,1s permanece real (39,06µs de fato entre
  amostras consecutivas).

## Ponto de transição (fim-de-vida, `>20g`)

Critério: primeiro instante (na série concatenada, ordem cronológica de
burst) em que `|accel_horizontal_g| > 20g` (critério dos organizadores
do desafio, Nectoux et al. 2012).

- Índice global (0-based) na série concatenada: **7.053.117**
- Valor no ponto de transição: **-20,816 g**
- Arquivo (1-based): **acc_02756.csv** (arquivo #2756 de 2803)
- Índice dentro do arquivo (0-based): **317**
- Nota: o canal horizontal já mostra picos >10g esporadicamente desde
  ~arquivo 2702 (degradação avançada visível bem antes do limiar de
  20g), e cruza 20g de forma transiente já no arquivo 2756 (`20,82g`)
  e 2762 (`20,96g`), recuando abaixo de 20g nos arquivos seguintes,
  antes de romper definitivamente acima de 20g a partir do arquivo 2766
  em diante (picos de até ~48g). A regra da metodologia ("primeiro
  instante que ultrapassa 20g") foi aplicada literalmente — usa o
  PRIMEIRO cruzamento transiente (arquivo 2756), não o cruzamento
  sustentado (arquivo 2766).

## Segmentos PRE/POST

- `PRE_full` = toda a série concatenada ANTES do índice de transição:
  **7.053.117 amostras**.
- `POST_full` = série concatenada A PARTIR do índice de transição
  (inclusive): **122.563 amostras** (~4,8s de gravação efetiva em 49
  bursts, dado que o teste FEMTO termina logo após o critério de
  fim-de-vida ser atingido).

## Decimação do PRE (desvio metodológico declarado, NÃO previsto em `METHODOLOGY_NOTE.md`)

`METHODOLOGY_NOTE.md` não antecipou segmentos PRE de ordem de
grandeza `~10^7` amostras. Benchmark real feito antes de qualquer
cálculo real (extrapolação de lei de potência a partir de N =
20k/50k/100k/200k, escala empírica ≈ N^1.48 para a implementação
via `cKDTree` de `mse_common.py`): uma ÚNICA chamada de
`sample_entropy` em `tau=1` sobre os 7.053.117 pontos do PRE completo
levaria ≈20 minutos — o protocolo `N_SURROGATES=200` do IAAFT (que
exige ordem de ~400 chamadas equivalentes só para o lado PRE) seria
inviável (~60+ horas).

**Decisão:** decimação por subamostragem uniforme por índice (stride),
fator `F=200`: `pre_decimated = pre_full[::200]`. NÃO é block-averaging
(distinto do próprio coarse-graining `tau` do MSE) — é um corte puro de
amostras, documentado aqui como simplificação computacional, não como
parte da metodologia de coarse-graining.

- `pre_decimated`: **35.266 amostras**.
- Usado como `PRE (primária)` na íntegra.
- `PRE (robustez)` = 50% mais recentes (por contagem) de `pre_decimated`
  → **17.633 amostras**.

O `POST` (122.563 / 61.281 amostras primária/robustez) foi mantido em
resolução NATIVA (sem decimação) — computacionalmente tratável
diretamente (benchmark: ~11s por `compute_mse` completo) e é o
segmento fisicamente mais importante (captura o transiente real de
falha).

## Arquivos salvos neste diretório

- `bearing1_1_horizontal_full_concat.npy` — canal horizontal completo,
  concatenado por burst em ordem cronológica, `float32`, 7.175.680
  amostras (arquivo bruto completo, decisão (a) acima, ANTES de
  qualquer decimação ou corte PRE/POST).
- `bearing1_1_horizontal_pre_decimated_f200.npy` — `PRE_full[::200]`,
  35.266 amostras, `float64` (a série `PRE primária` efetivamente usada
  no pipeline).
- `bearing1_1_horizontal_post_full.npy` — `POST_full`, 122.563 amostras,
  `float64` (a série `POST primária` efetivamente usada no pipeline,
  sem decimação).

Os 2.803 arquivos brutos `acc_XXXXX.csv` individuais NÃO foram salvos
neste repositório (219MB, redundante com o array concatenado acima);
podem ser re-obtidos do mirror/commit citados acima a qualquer momento.
