# Nota de metodologia — fechamento dos 3 gaps de `critical-slowing-down`

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 3 domínios (GISP2, PhysioNet SDDB, NASDAQ). Este arquivo é commitado
antes da execução da análise, no mesmo espírito de disciplina de
pré-registro já usado no laboratório (mesmo que este ainda seja um passo
de Fase 0/exploratório, não um `PREREGISTRATION.md` formal travado).

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md` para o
levantamento que identificou os 3 gaps a fechar: (a) regra única de
seleção de `lambda` cross-domain; (b) protocolo de teste contra nulo
substituto; (c) cálculo real de `Delta I` nos 3 domínios já verificados
(GISP2, PhysioNet SDDB, NASDAQ).

## Gap (a): regra de `lambda` cross-domain

**Decisão:** todos os parâmetros de escala são expressos como FRAÇÕES
adimensionais do comprimento do segmento de análise, nunca em unidades
físicas absolutas (anos, segundos, amostras) — esta é a convenção padrão
já usada na literatura de early-warning-signals (Dakos, V., Carpenter,
S.R., Brock, W.A., Ellison, A.M., Guttal, V., Ives, A.R., Kéfi, S.,
Livina, V., Seekell, D.A., van Nes, E.H., Scheffer, M. (2012). "Methods
for Detecting Early Warnings of Critical Transitions in Time Series
Illustrating Sliding Window and Young's method." *PLOS ONE* 7(7):e41010 —
e a implementação de referência no pacote R `earlywarnings`), não uma
convenção inventada nesta sessão. Valores fixados a priori, os MESMOS
para os três domínios:

- `bandwidth_frac = 0.20` — largura de banda do suavizador Gaussiano
  usado para destendenciar a série (remover a tendência lenta antes de
  medir AC1/variância dos resíduos).
- `window_frac = 0.50` — tamanho da janela deslizante para estimar
  AC1/variância, como fração do comprimento do segmento (convenção
  "half-length rolling window" de Dakos et al.).
- `step_frac = 0.02` — passo do deslizamento da janela, como fração do
  comprimento do segmento.

Todos os três valores são reaproveitados sem nenhum reajuste entre os
domínios — a mesma implementação (`analysis/csd_common.py`) é chamada sem
modificação em GISP2, PhysioNet SDDB e NASDAQ.

**Definição do segmento pré-transição (decisão adicional, necessária para
operacionalizar a regra acima):** duas variantes, ambas fixadas a priori
e AMBAS reportadas sempre juntas (nunca escolhendo a mais favorável
depois de ver o resultado):

1. **Primária:** todo o registro contínuo disponível anterior ao
   timestamp de transição documentado pela própria fonte.
2. **Robustez:** os 50% mais recentes (mais próximos da transição) desse
   mesmo segmento primário — ainda uma fração fixa e cega ao domínio, não
   uma data escolhida à mão por análise visual dos dados de cada domínio
   (o que seria uma forma de viés de confirmação).

**Limitação honesta declarada a priori:** a variante primária, para
registros muito longos com múltiplas transições anteriores não
relacionadas dentro do mesmo dado bruto (ex. GISP2 tem 49.000 anos com
vários eventos Dansgaard-Oeschger antes de Younger Dryas; NASDAQ tem 30
anos com o crash de 1987 e outros ciclos antes da bolha pontocom), pode
diluir qualquer sinal de CSD específico da transição-alvo com ruído/
tendência de eventos anteriores não relacionados. Isso é reportado como
risco conhecido, não escondido — e é exatamente por isso que a variante
de robustez (50% mais recentes) existe como checagem complementar, não
como substituição seletiva.

## Gap (b): protocolo de teste contra nulo substituto

**Decisão:** método de Dakos et al. (2008) *PNAS* 105(38):14308-14312,
Materiais e Métodos — o mesmo método já citado no levantamento de Fase 0:

1. Ajustar um processo AR(1) de PARÂMETRO CONSTANTE (`x_{t+1} = a·x_t +
   ε_t`, `ε_t ~ N(0,σ²)`) aos resíduos destendenciados do segmento
   inteiro, por mínimos quadrados de um passo. `a` e `σ` são estimados
   UMA VEZ para o segmento todo (nenhuma tendência temporal é imposta ao
   processo nulo — essa é a definição operacional do modelo concorrente
   "sem CSD": memória curta de parâmetro fixo).
2. Gerar `N_SURROGATES = 1000` realizações sintéticas desse processo
   AR(1) de parâmetro constante, mesmo comprimento do segmento real.
3. Rodar a MESMA pipeline de janela deslizante (mesmas frações da Seção
   anterior) em cada substituto, obtendo a estatística de tendência
   (`tau` de Kendall de AC1 vs. posição da janela, e separadamente de
   variância vs. posição) para cada um dos 1000 substitutos.
4. Comparar o `tau` real contra a distribuição nula dos 1000 substitutos:
   `p = fração de substitutos com tau_substituto >= tau_real` (teste
   unicaudal, já que CSD prevê especificamente uma tendência POSITIVA de
   AC1/variância aproximando-se da transição, não qualquer tendência).
5. Semente do gerador de números aleatórios fixada (`seed=12345`) e
   documentada, para reprodutibilidade exata por qualquer reexecução
   adversarial futura.

## Gap (c): cálculo real de `Delta I`

Depois de (a) e (b) fixados e commitados, `Delta I` será calculado nos 3
domínios já verificados na Fase 0 (URLs e notas de verificação de acesso
em `phase0/PHASE0_SURVEY.md`):

1. GISP2 (NOAA/WDS Paleoclimatology, `gisp2_temp_accum_alley2000.txt`) —
   transição Younger Dryas→Preboreal, ~11,5 kyr BP.
2. PhysioNet SDDB, registro 30 — onset de fibrilação ventricular em
   07:54:33 (anotado no próprio cabeçalho `.hea`).
3. NASDAQ Composite (FRED `NASDAQCOM`) — pico da bolha pontocom em
   2000-03-10.

## O que este passo NÃO é

Isto continua sendo trabalho de Fase 0/exploratório — `DISC-TRI-RG-001`
segue `CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum
`PREREGISTRATION.md` foi travado. Nenhuma alegação de "descoberta
confirmada" será feita a partir deste resultado sozinho — o objetivo é
verificar se há sinal real o suficiente para justificar escrever e travar
um pré-registro formal (com holdout declarado para o Gate de Replicação
futuro, usando um evento de transição ainda não tocado). A metodologia
acima foi fixada ANTES de qualquer cálculo, precisamente para que, se um
pré-registro for escrito depois, ele possa declarar honestamente que a
regra de escala e o protocolo de nulo já existiam antes de qualquer
resultado ser visto — mesmo que a base de dados primária (não um holdout
novo) seja a mesma usada aqui.
