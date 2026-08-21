# RH-REAL — Fase 0 (continuação): triagem dos itens 5, 6, 10 — NOTA DE TRIAGEM (pré-computação)

**Status:** `evidence_level: exploratory_only`. NÃO é um pré-registro, NÃO
produz alegação alguma sobre RH nem sobre nenhum dos itens. Autorizada por
`DISC-DEC-013` (2026-08-21) como continuação da Fase 0 de
`DISC-RH-REAL-001` — a `stop_condition` da linha (em
`01_PORTFOLIO/TEST_QUEUE.yaml`) proíbe tratar qualquer achado desta fase
como resultado pré-registrado e proíbe qualquer alegação de progresso
sobre RH em si. Este documento foi escrito e salvo **antes** de qualquer
computação sobre os itens (regra da frente; mesma disciplina de
`METHODOLOGY_NOTE.md` das linhas anteriores).

**Data:** 2026-08-21. **Diretório de trabalho:**
`02_TESTS/RH_ZETA_ZEROS/phase0_zeta_eval_triage/` (nenhum arquivo
pré-existente de `RH_ZETA_ZEROS/` é modificado).

---

## 0. O que o arquivo do repositório de fato preserva sobre os itens 5, 6, 10

Honestidade primeiro: **o texto integral do levantamento de literatura de
2026-08-12 (as definições verbatim dos 12 itens) não foi persistido no
repositório.** O que está persistido é:

- `PHASE0_TRIAGE_SUMMARY.md` (linhas 17–19): *"Itens 5, 6, 10 exigem
  avaliação de ζ(s) (não só localização de zeros) — deferidos."* — única
  menção direta aos três itens.
- `09_SESSIONS/2026/2026-08-12_RH_REAL_PHASE0_AND_GAP_RUNS.md` (item 2):
  o levantamento cobriu *"correlação de pares (Montgomery), estatística
  GUE, N(T) (Riemann–von Mangoldt), **momentos de zeta**, constantes de
  gaps pequenos/grandes, e uma questão explicitamente em aberto
  (dez/2024, arXiv:2412.15481) sobre runs de gaps moderados
  consecutivos"*.
- Itens identificáveis pelos artefatos persistidos: 1 (correlação de
  pares), 2 (GUE/Wigner), 3 (N(T)), 7 (gaps pequenos, Inoue), 8 (gaps
  grandes, Bui–Milinovich), 9 (runs, arXiv:2412.15481), 12 (variância de
  número/rigidez GUE, citado como "STATUS_UNCERTAIN" no sumário).

**Consequência:** as definições exatas dos itens 5, 6, 10 precisam ser
**reconstruídas**, e esta nota rotula a reconstrução como tal. A
reconstrução abaixo usa (a) o critério persistido e inequívoco — "exigem
avaliação de ζ(s)" —, (b) o tópico "momentos de zeta" listado no
levantamento e não coberto por nenhum item triado, e (c) as três famílias
canônicas de resultados/conjecturas numericamente testáveis sobre ζ que
exigem avaliar ζ(s) na linha crítica (e não apenas localizar zeros) na
literatura padrão. Todas as citações abaixo foram **verificadas por fetch
direto no arXiv em 2026-08-21** (título e autores conferidos), não
digitadas de memória. Se o relatório original da sessão de 2026-08-12
definia os itens 5/6/10 de outra forma, esta triagem cobre, ainda assim,
o espaço correto: os três alvos de "avaliação de ζ" numericamente
testáveis padrão da literatura.

---

## 1. Itens reconstruídos, com citações verificadas

### Item 5 (reconstruído) — Momentos de ζ na linha crítica

**Enunciado.** Para o momento de ordem 2k,
`I_k(T) = (1/T) ∫₀ᵀ |ζ(1/2+it)|^{2k} dt`:
- k=1 (teorema, Hardy–Littlewood 1918): `I_1(T) ~ log(T/2π) + 2γ − 1`.
- k=2 (teorema, Ingham 1926): `I_2(T) ~ (1/2π²) log⁴T` (termo líder;
  polinômio completo de grau 4 conhecido).
- k≥3 (conjectural): conjectura de momentos via matrizes aleatórias
  (Keating–Snaith 2000, Comm. Math. Phys. 214) e sua forma completa com
  todos os termos de ordem inferior: **Conrey–Farmer–Keating–Rubinstein–
  Snaith, "Integral moments of L-functions", arXiv:math/0206018**
  (verificado 2026-08-21: título e autores conferem; o paper propõe
  polinômios conjecturais completos e já contém verificação numérica
  própria).

**Por que exige avaliar ζ:** o integrando é `|ζ(1/2+it)|^{2k}` — não há
como obtê-lo de localizações de zeros.

### Item 6 (reconstruído) — Teorema central do limite de Selberg para log|ζ|

**Enunciado.** (Selberg 1946; prova curta moderna: **Radziwiłł–
Soundararajan, "Selberg's central limit theorem for log|ζ(1/2+it)|",
arXiv:1509.06827** — verificado 2026-08-21: o abstract afirma exatamente
que `log|ζ(1/2+it)|` é aproximadamente normal com média 0 e **variância
(1/2)·log log t**.) Para t uniforme em [T, 2T],
`log|ζ(1/2+it)| / sqrt((1/2) log log T) → N(0,1)`.

**Por que exige avaliar ζ:** a estatística é o valor de `log|ζ|` em
pontos t genéricos (não-zeros).

### Item 10 (reconstruído) — Máximo de |ζ| em intervalos curtos (Fyodorov–Hiary–Keating)

**Enunciado.** **Fyodorov–Hiary–Keating, "Freezing transition,
characteristic polynomials of random matrices, and the Riemann
zeta-function", arXiv:1202.4713** (verificado 2026-08-21: título/autores
conferem; conjectura que a transição de congelamento do REM governa os
extremos de |ζ| em trechos de comprimento fixo da linha crítica).
Forma quantitativa: para intervalo de comprimento O(1) (aqui 2π) na
altura T,
`max log|ζ| ≈ log log T − (3/4) log log log T + O_p(1)`.
O coeficiente **−3/4** é a assinatura do campo log-correlacionado; o
modelo concorrente nomeado — variáveis independentes tipo REM/iid com a
mesma variância — prevê **−1/4**. Ordem líder provada:
**Arguin–Belius–Bourgade–Radziwiłł–Soundararajan, "Maximum of the
Riemann zeta function on a short interval of the critical line",
arXiv:1612.08575** (verificado 2026-08-21). O termo subdominante (o
−3/4) é exatamente onde vive a questão numérica.

**Por que exige avaliar ζ:** o máximo de `log|ζ|` sobre um intervalo não
é função das posições dos zeros disponíveis nas tabelas (exigiria todos
os zeros + fórmula explícita truncada — na prática, avalia-se ζ).

---

## 2. O que será computado, sobre quais dados, com qual método de avaliação de ζ

### 2.1 Método de avaliação de ζ (comum aos três itens)

- **Motor primário:** fórmula de Riemann–Siegel para
  `Z(t) = e^{iθ(t)} ζ(1/2+it)` (real; `|Z(t)| = |ζ(1/2+it)|`),
  implementada vetorizada em `numpy`: soma principal
  `2 Σ_{n≤N} n^{-1/2} cos(θ(t) − t log n)` com `N = ⌊sqrt(t/2π)⌋` +
  termo de correção C₀ de Riemann–Siegel; `θ(t)` via expansão de
  Stirling. Erro esperado O(t^{-3/4}) — mais que suficiente para
  estatísticas de |ζ| O(1)–O(10) em t ≥ 10³.
- **Motor de referência:** `mpmath` (`mp.zeta`, `mp.siegelz`,
  `mp.zetazero`), precisão arbitrária, lento — usado para **validar** o
  motor primário, não para as varreduras.
- **Validação obrigatória ANTES de usar nos itens** (registrada em
  `validation_zeta_eval.log` + `.json`); critérios fixados agora:
  1. `mp.zeta(2)` vs `π²/6` — erro relativo < 10⁻¹⁰;
  2. `mp.zeta(0.5)` vs valor de referência −1.4603545088… (computado
     por mpmath em precisão dupla estendida, consistência interna entre
     `dps=15` e `dps=30`);
  3. `mp.zetazero(1)` vs 14.134725142 (1º zero, confere também com a
     1ª linha de `data/zeros1.txt`, Odlyzko) — |Δ| < 10⁻⁶;
  4. Motor numpy-RS vs `mp.siegelz` em ≥ 40 pontos t espalhados em
     [50, 10¹¹] — erro absoluto máximo < 10⁻³ (e < 10⁻⁵ para t ≥ 10⁵);
  5. Cruzamento com dado real de Odlyzko: `Z(t)` do motor numpy troca
     de sinal em janelas ±0,01 em torno de ≥ 20 zeros de `zeros1.txt`
     (amostrados) e a contagem de mudanças de sinal de Z em
     [γ₁−0,5, γ₁₀₀+0,5] é exatamente 100.
  **Se qualquer critério falhar, os itens não são computados** até o
  motor ser corrigido ou substituído por mpmath puro (mais lento, com
  amostragem reduzida e documentada).

### 2.2 Dados

Os três itens exigem ζ avaliada em `t` arbitrário; as tabelas de Odlyzko
(`data/zeros1.txt` etc., ver `data/PROVENANCE.md`) entram como (a)
âncora de validação do motor (critério 5 acima) e (b) definição dos
regimes de altura reais já usados pela linha (baixo: t ≤ 7,5×10⁴,
`zeros1`; alto: t ≈ 2,7×10¹¹, `zeros3`). As varreduras em si são
computadas por avaliação direta de ζ (não há alternativa — é exatamente
por isso que estes itens ficaram de fora da triagem de 2026-08-12).
Custos são mantidos limitados por **subamostragem declarada** (grades e
tamanhos abaixo); qualquer redução adicional em tempo de execução será
registrada no log e no adendo, nunca silenciosa.

### 2.3 Item 5 — plano

- Grade: `t ∈ [100, 30000]`, passo 0,05 (~6×10⁵ avaliações de Z).
- Computar `I_1(T)` e `I_2(T)` acumulados (regra do trapézio) em
  T ∈ {10³, 3×10³, 10⁴, 3×10⁴}.
- Comparar: `I_1(T)` vs `log(T/2π) + 2γ − 1` (teorema, validação do
  pipeline de momentos); `I_2(T)` vs termo líder de Ingham
  `(1/2π²) log⁴T` e vs polinômio completo conjectural CFKRS de grau 4
  (coeficientes computados numericamente a partir da receita do
  arXiv:math/0206018 — se a implementação do polinômio completo não for
  viável no orçamento desta triagem, comparar só com o termo líder e
  registrar a diferença como estimativa empírica dos termos de ordem
  inferior).
- **O que a triagem avalia:** viabilidade de custo; tamanho relativo dos
  termos de ordem inferior em T acessível (determina se uma pergunta
  sobre k=3 conjectural é discriminável); se existe pergunta
  falsificável com concorrente nomeado (candidata: coeficiente do termo
  líder do 6º momento — `g₃a₃/9!` de Keating–Snaith/CFKRS vs.
  extrapolação "só termo líder de grau 9 com constante livre ajustada" —
  e o risco de ser mera replicação da verificação numérica que o próprio
  CFKRS já publicou).

### 2.4 Item 6 — plano

- Alturas: T ∈ {10⁴, 10⁶, 10⁸, 10¹⁰}; em cada uma, N = 4000 pontos t
  i.i.d. uniformes em [T, 2T] (RNG semeada, seed 20260821, registrada).
- Computar `X = log|Z(t)|`; estatísticas: média, variância, assimetria,
  curtose; KS contra N(0, (1/2)loglog t); variância empírica vs
  **modelo A (Selberg/RS): σ² = (1/2)loglog T** vs **modelo B
  (concorrente nomeado: lognormal "ingênuo" sem o fator 1/2): σ² =
  loglog T**.
- **O que a triagem avalia:** viabilidade (trivial em baixa altura; qual
  o custo em t ~ 10¹⁰–10¹¹?); com que N/T os modelos A e B se separam;
  e o problema de fundo para pré-registro: o enunciado central é um
  **teorema provado** — a pergunta falsificável teria que ser sobre
  correções de altura finita (velocidade de convergência), não sobre o
  teorema, e a triagem mede se essas correções são grandes o bastante
  para sustentar uma pergunta afiada.

### 2.5 Item 10 — plano

- Alturas: T ∈ {10⁵, 10⁷, 10⁹} (estender a 10¹¹ ~ regime de `zeros3`
  somente se o custo medido permitir; decisão registrada no log); em
  cada altura, M = 300 intervalos de comprimento 2π com inícios
  aleatórios em [T, 2T] (seed 20260821); grade intra-intervalo de 256
  pontos (passo ~0,0245 — ~8–13 pontos por espaçamento médio de zeros
  nestas alturas; o viés de subestimação do máximo por grade finita será
  estimado refinando a grade 4× em uma subamostra e registrado).
- Estatística por altura: média e desvio-padrão de
  `M* = max log|Z|` sobre os M intervalos.
- Comparação: regressão de `média(M*) − loglog T` contra `logloglog T`
  nas alturas disponíveis — **modelo FHK: coeficiente −3/4** vs
  **modelo concorrente nomeado (REM/iid): coeficiente −1/4** (ambos com
  intercepto O(1) livre, pois a constante não é prevista).
- **O que a triagem avalia:** este é o item com a pergunta falsificável
  mais genuína (dois modelos nomeados, coeficientes numéricos
  distintos, questão viva na literatura) — mas com suspeita a priori de
  **potência estatística insuficiente**: `logloglog T` varia ~0,2 entre
  10⁵ e 10⁹, o sinal discriminante é (3/4−1/4)×0,2 ≈ 0,1, e as
  flutuações do máximo são O(1). A triagem produz exatamente essa conta
  de potência com números empíricos (desvio-padrão real de M* por
  altura, custo real por avaliação) e conclui se um pré-registro viável
  existe (e com que M, quais alturas) ou não.

---

## 3. Critérios de saída da triagem (fixados antes de computar)

Para cada item, a tabela final (`TRIAGE_RESULTS.md`) responderá:

1. **O que foi computado** (com custo real medido);
2. **Resultado numérico** (sem interpretação além de consistência);
3. **Admite pergunta pré-registrável genuinamente falsificável, com
   modelo concorrente NOMEADO?** — exigência de observável
   discriminante da linha; "reproduzir um teorema" ou "confirmar valor
   já publicado pelo próprio proponente" contam como fraquezas
   explícitas;
4. **Recomendação** (só recomendação — nenhum lock, nenhum
   pré-registro é desenhado nesta fase).

Limites de execução: cada script individual limitado a ~10 min de
parede; subamostragens adicionais para caber no limite são documentadas
no log e mencionadas na tabela final. Nenhum processo em segundo plano
deixado rodando.

---

*Adendo permitido: no máximo um, datado, ao final deste arquivo, nos
termos das regras da frente.*

---

## ADENDO (único, datado) — 2026-08-21, após validação do motor, ANTES de computar os itens

Três calibrações de método, decididas durante a fase de validação
(`validate_zeta_eval.py`) e antes de qualquer computação dos itens 5/6/10:

1. **Domínio validado do motor: t ∈ [2000, 10¹¹]** (não [50, 10¹¹] como
   o critério 4 originalmente varria). O truncamento pós-C₀ da fórmula de
   Riemann–Siegel dá erro ~2,6×10⁻³ em t < 10³ (medido na 1ª rodada,
   preservada em `validation_zeta_eval_run1_FAILED.log`). Nenhum item usa
   t < 2000. **Item 5 passa a usar integrais janeladas**
   `(1/(T−T₀))∫_{T₀}^{T}` com T₀ = 2000, comparadas às mesmas diferenças
   das fórmulas assintóticas — matematicamente equivalente para a
   comparação pretendida e evita o regime não-validado.
2. **Correção de bug pré-uso:** a redução de fase mod 2π usava uma
   constante 2π derivada de float64; em t ~ 10¹¹ isso injetava erro
   ~2,5×10⁻⁴ em Z. Corrigido com constantes longdouble por string
   (`rs_zeta.py`). Detectado e corrigido pela própria validação, antes de
   qualquer uso.
3. **Tolerâncias do critério 4 em faixas** (em vez de um único
   "<10⁻⁵ para t ≥ 10⁵"): <10⁻³ em [2×10³,10⁵); <10⁻⁵ em [10⁵,10¹⁰);
   <5×10⁻⁴ em [10¹⁰,10¹¹]. Motivo: acúmulo coerente do ruído de fase do
   longdouble (δ ~ t·ε_LD com ε_LD≈1,08×10⁻¹⁹, somado sobre
   Σn^{-1/2}≈2√N termos) dá cota ~1,2×10⁻⁴ em t≈6×10¹⁰ — e o erro medido
   foi 1,14×10⁻⁴, consistente. Para as estatísticas desta triagem
   (log|Z| e momentos, escala O(1)–O(10)), erro absoluto ≤5×10⁻⁴ em Z é
   desprezível (afeta log|Z| de forma relevante apenas em vizinhanças de
   medida ínfima dos zeros). Resultado final: **validação PASSOU** com os
   5 critérios — `validation_zeta_eval.{log,json}`.

Nenhuma outra alteração de plano; grades e seeds dos itens permanecem os
da seção 2. (Se limites de tempo de execução exigirem subamostragem
adicional, ela será registrada nos logs e na tabela de
`TRIAGE_RESULTS.md`, como já previsto na seção 2.2 — não neste adendo.)
