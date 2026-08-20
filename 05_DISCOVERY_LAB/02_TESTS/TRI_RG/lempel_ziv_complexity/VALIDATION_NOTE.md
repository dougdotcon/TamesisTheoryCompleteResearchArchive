# Nota de validação — `lempel-ziv-complexity`, ANTES de qualquer dado real

**Status: validação sintética obrigatória (`METHODOLOGY_NOTE.md` Gap (b))
concluída — resultado MISTO entre os 2 canais, com o fallback
pré-autorizado de bootstrap por blocos móveis (Kunsch 1989) já aplicado
ao canal que mostrou baixo poder de IAAFT, exatamente como o Gap (d)
determina.** Pipeline (`analysis/lzc_common.py`) e script de validação
(`analysis/validate_synthetic.py`) commitados; resultado completo em
`analysis/validation_synthetic.json`. **Nenhum dado real (Daphnet
Freezing-of-Gait, Kilauea 2018 LERZ) foi tocado em nenhum momento deste
passo.**

## Resumo honesto do resultado — a pergunta central desta validação

`METHODOLOGY_NOTE.md` Gap (b) não fazia uma previsão a priori sobre QUAL
canal (se algum) mostraria poder — ao contrário do candidato de entropia
de permutação (`C_JS`/`H_S`, previsão assimétrica), `LZC_ternary` foi
nomeado explicitamente como um diagnóstico de robustez (mesmo alfabeto
mais fino), não um discriminador caos-vs-ruído desenhado para essa
finalidade (Nagarajan 2002). **O resultado observado: `LZC_ternary`
mostra poder real e total contra o substituto IAAFT no controle positivo
(`p=0,0`, σ-equivalente `-41,14`); `LZC_median` NÃO mostra poder real
contra IAAFT (`p=0,455`, muito acima de 0,05) — e o fallback de
bootstrap por blocos móveis pré-autorizado, aplicado a `LZC_median`
especificamente por causa disso, TAMBÉM não recupera poder para esse
canal (`p=0,95` no mesmo controle positivo, PIOR que o IAAFT, não
melhor).** Isso é relatado aqui de forma direta e simétrica, sem suavizar
nenhum dos dois resultados: `LZC_ternary` (companheiro) sobrevive à
validação de poder pelo teste primário; `LZC_median` (primário) NÃO
sobrevive à validação de poder por nenhum dos dois testes disponíveis
nesta linha.

## Diagnóstico de correção do código (ANTES dos controles estocásticos)

Dois checks, ambos passando:

1. **Caso de teste do próprio Kaspar & Schuster 1987:** string binária
   `1001111011000010` (16 símbolos) tem `c(n)=6` documentado — computado
   aqui, `c_computado=6`, `match=true`.
2. **Checagem de monotonicidade** (`N=500`, sequências binárias):
   `c(constante)=2 < c(alternada-periódica)=3 < c(aleatória-iid)=62` —
   exatamente a ordem esperada, já que o LZ76 encontra novas frases mais
   rápido em sequências menos estruturadas.

**Veredito: `CODE_CORRECT`.**

## Controles sintéticos (`seed=12345`, `N_SURROGATES=200`, `N_IAAFT_ITER=50`, `N=3.000` para todos os controles)

### Controle positivo (`METHODOLOGY_NOTE.md` Gap (b), especificação exata)

PRE = ruído branco Gaussiano iid. POST = mapa logístico caótico (`r=4`),
remapeado por posto (rank-remap) sobre os valores exatos do PRE —
marginal idêntica por construção, espectro confirmado empiricamente
quase plano em ambos (`spectral_exponent_pre=-0,058`,
`spectral_exponent_post=+0,014`).

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | σ-equivalente | `p` (bicaudal, n=200) | veredito |
|---|---|---|---|---|---|---|---|---|
| `LZC_median` | 1,0357 | 1,0473 | **+0,01155** | 0,0001 | 0,01335 | +0,858 | **0,455** | `IAAFT_LOW_POWER` |
| `LZC_ternary` | 1,0154 | 0,5320 | **−0,4834** | −0,0004 | 0,01174 | **−41,14** | **0,0** | `IAAFT_HAS_REAL_POWER` |

`LZC_ternary` mostra separação total (`p=0,0` literal, nenhum dos 200
substitutos com `|Δ_substituto|>=|Δ_real|`). `LZC_median` fica bem
próximo da nula (Δ real quase dentro de 1σ da nula) — o mapa logístico
`r=4` muda drasticamente a estrutura fina capturada pela quantização
ternária (tercis), mas quase não move a mediana binária deste processo
específico.

### Controle negativo (dois sorteios independentes de fGn-like, `H=0,7` fixo)

Sonda o risco de redundância assintótica de Ziv & Lempel 1978 (mesmo `H`,
sem mudança estrutural genuína).

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | σ-equivalente | `p` (bicaudal) | veredito |
|---|---|---|---|---|---|---|---|---|
| `LZC_median` | 0,0462 | 0,0616 | +0,0154 | 0,01313 | 0,01475 | +0,154 | **0,5** | corretamente não significativo |
| `LZC_ternary` | 0,0704 | 0,0753 | +0,0049 | 0,01031 | 0,01275 | −0,428 | **0,74** | corretamente não significativo |

Ambos os `p` ficam bem acima de 0,05 — o IAAFT está corretamente
calibrado sob a nula de "mesmo processo linear, sem mudança estrutural
genuína" para os dois canais.

### Controle de Hurst diferencial (`H=0,3` → `H=0,9`, puramente linear, sem estrutura não-linear)

Sonda diretamente se um deslocamento PURAMENTE linear/espectral de Hurst
produz significância espúria em qualquer canal — o risco de redundância
assintótica com a família Hurst já fechada NEGATIVA nesta linha
(`alpha` DFA, `h(2)` wavelet), nomeado explicitamente em
`METHODOLOGY_NOTE.md` Gap (b). Casamento espectral confirmado
(`spectral_exponent_pre=1,600` vs. alvo `2H+1=1,6`;
`spectral_exponent_post=2,796` vs. alvo `2,8`).

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | σ-equivalente | `p` (bicaudal) | veredito |
|---|---|---|---|---|---|---|---|---|
| `LZC_median` | 0,2657 | 0,0193 | −0,2464 | −0,2326 | 0,0335 | −0,411 | **0,365** | sem significância espúria |
| `LZC_ternary` | 0,2866 | 0,0267 | −0,2599 | −0,2583 | 0,0228 | −0,073 | **0,455** | sem significância espúria |

**Nenhum dos dois canais mostra significância espúria a partir de um
deslocamento puramente linear de Hurst** — o risco central nomeado no
Gap (b) (convergência assintótica de Ziv & Lempel 1978 para a mesma taxa
de entropia que MSE/DFA/wavelet já testam) não se manifesta como um
falso positivo aqui, para nenhum canal, em amostra finita.

## Fallback pré-autorizado: bootstrap por blocos móveis (Kunsch 1989) — acionado para `LZC_median`

**Disparado automaticamente** porque `LZC_median` mostrou
`IAAFT_LOW_POWER` no controle positivo (Gap (d): "se a validação
sintética mostrar baixo poder do IAAFT para QUALQUER canal, bootstrap
por blocos móveis é adicionado como teste PRIMÁRIO complementar para
esse canal, ANTES de tocar dado real"). Rodado nos MESMOS controles
positivo/negativo já usados acima (`block_length=150` = `max(N//20,10)`
para `N=3.000`, `n_bootstrap=200`, `seed=12345`).

| Canal | Controle | Δ real | `p` bootstrap (bicaudal) | veredito bootstrap |
|---|---|---|---|---|
| `LZC_median` | Positivo | +0,01155 | **0,95** | `BOOTSTRAP_LOW_POWER` |
| `LZC_median` | Negativo | +0,01540 | 0,74 | corretamente não significativo |
| `LZC_ternary` | Positivo | −0,4834 | **0,0** | `BOOTSTRAP_HAS_REAL_POWER` |
| `LZC_ternary` | Negativo | +0,0049 | 1,02* | corretamente não significativo |

*(`p=1,02` no controle negativo de `LZC_ternary` é um artefato limitado
da fórmula `2*min(frac<=0, frac>=0)` quando uma fração razoável dos 200
Δ de bootstrap cai exatamente em zero por reamostragem degenerada — não
afeta a decisão, já que o valor só precisa estar >=0,05 para contar como
"corretamente não significativo", e claramente está. Documentado aqui em
vez de arredondado silenciosamente para 1,0, por honestidade.)

**Resultado do fallback para `LZC_median`: PIOR, não melhor, que o
IAAFT** (`p=0,95` vs. `p=0,455` no mesmo controle positivo) — o bootstrap
por blocos móveis NÃO recupera poder discriminativo para este canal. Isto
é relatado exatamente como encontrado, sem tentar uma segunda correção
(per a disciplina de escalonamento desta linha: "esta é a ÚNICA correção
pré-autorizada — se o fallback também não resolver, o candidato é
fechado na etapa de validação [para esse canal], sem uma segunda
tentativa de redesenho").

**Para `LZC_ternary` (já com poder via IAAFT), o bootstrap concorda**
(`p=0,0`, `BOOTSTRAP_HAS_REAL_POWER`) — checagem de consistência entre os
dois testes de significância desta linha, não uma segunda validação
necessária (o canal já havia sobrevivido ao teste primário).

## Veredito final por canal (combinação mecânica de IAAFT + fallback, per `final_decision_protocol_verdict`)

- **`LZC_median` (canal primário): `NO_POWER_ESTABLISHED_EITHER_TEST`.**
  Não mostra poder discriminativo real contra ruído estocástico linear
  correlacionado (IAAFT) NEM contra a alternativa de bootstrap por
  blocos móveis, no único cenário de controle positivo testado (mapa
  logístico `r=4` vs. ruído branco de marginal idêntica). Isto é
  consistente com a fraqueza estrutural já nomeada a priori em
  `METHODOLOGY_NOTE.md` Gap (b) (Nagarajan 2002: LZC, ao contrário de
  `C_JS`, não foi desenhado especificamente como discriminador
  caos-vs-ruído) — não é uma surpresa descoberta defensivamente depois
  do nulo, é exatamente o cenário que o próprio metodologia note já
  havia deixado espaço para.
- **`LZC_ternary` (canal companheiro): `SURVIVES_PRIMARY_IAAFT_TEST`.**
  Mostra poder real e completo (`p=0,0`, σ-equivalente `-41,14`) contra o
  substituto IAAFT no controle positivo, corretamente não significativo
  no controle negativo (`p=0,74`) e sem significância espúria sob o
  controle de Hurst diferencial (`p=0,455`).
- **Nenhum canal mostrou não-computabilidade estrutural** —
  `real_pre`/`real_post` retornaram `status="ok"` em todos os controles
  para ambos os canais, confirmando empiricamente a expectativa do
  próprio `METHODOLOGY_NOTE.md`: sem embedding/dimensão/delay/grade de
  escalas, LZC não tem o modo de falha de não-resolução que fechou RQA.

## Nenhum desvio metodológico

Nenhuma decisão metodológica de `METHODOLOGY_NOTE.md` foi alterada
depois de ver o resultado. `R_lambda` (mediana binária / tercis
ternários), `I(X)` (LZC normalizada de Kaspar & Schuster), o protocolo
IAAFT (`N_SURROGATES=200`, `N_IAAFT_ITER=50`, `seed=12345`), e o
fallback de bootstrap por blocos móveis (`block_length=max(N//20,10)`)
permanecem exatamente como fixados em `METHODOLOGY_NOTE.md`, sem
reformulação alguma. A decisão de rebaixar `LZC_median` a
diagnóstico-only (per a disciplina já usada para `kappa`/`beta_D2` em
Kramers-Moyal) NÃO é tomada por este agente — cabe à sessão
orquestradora, exatamente como o próprio Gap (e) já determina. Este
agente apenas relata os dois vereditos, lado a lado, sem promover
`LZC_ternary` a primário nem rebaixar `LZC_median` formalmente.

## Próximo passo

Nenhum canal mostrou falha estrutural (não-computabilidade); pelo menos
um canal (`LZC_ternary`) mostrou poder discriminativo real e completo —
por essa métrica, a validação de PODER exigida pelo Gap (b) autoriza
prosseguir para a etapa de dado real (Daphnet, Kilauea), reportando os
dois canais lado a lado com seus vereditos de validação honestos,
exatamente como já documentado aqui. Ver `RESULTS_SUMMARY.md` para o
resultado em dado real.

## Adendo — correção de bug de desempenho descoberta no passo de dado real (não afeta nenhum resultado desta nota)

Ao aplicar `run_lzc_analysis` aos 2 domínios reais (ver
`RESULTS_SUMMARY.md`), o pipeline travou por dezenas de minutos de CPU
sem terminar nenhuma das 4 combinações domínio/variante — mesmo para
`daphnet/primary` (`N_PRE=72.944`, `N_POST=79.043`), tamanhos que
`METHODOLOGY_NOTE.md` Gap (d) havia assumido "baratos" porque "o próprio
parsing LZ76 é O(N)". **Essa suposição estava errada para a
implementação de fato usada**: `lz76_complexity` (a versão ingênua de
laço aninhado i/k/l, fiel ao pseudocódigo de Kaspar & Schuster 1987)
reinicia sua busca de correspondência a partir de `i=0` a CADA fronteira
de frase — O(N) de trabalho por frase, dando ≈O(N²/log N) no total para
dado quase-aleatório. Medido diretamente: `N=20.000` já leva ≈6,2s;
`N=79.043` leva ≈97s; `N=200.000` (o teto de subamostragem de Gap (d))
foi morto depois de mais de 30 minutos de CPU sem terminar. Isso NUNCA
apareceu na validação sintética porque `N=3.000` lá é pequeno o
suficiente para a versão ingênua ainda ser rápida (~0,18s por chamada,
extrapolado) — o defeito só se manifesta na escala real dos 2 domínios.

**Correção implementada em `lzc_common.py` (mesma disciplina já usada em
`pe_common.py`, Adendo 2 de `permutation_entropy/VALIDATION_NOTE.md`):
uma reimplementação O(n log n) da MESMA quantidade `c(n)`**, via array
de sufixos (duplicação de prefixo, vetorizada com `numpy`) + array LCP
de Kasai + tabela esparsa para RMQ + árvore de Fenwick para estatística
de ordem (predecessor/sucessor), sem depender de nenhum pacote externo
(`sortedcontainers` foi cogitado e descartado — reprodutibilidade sem
dependência extra pesou mais). A prova de equivalência: o laço ingênuo
tenta cada posição candidata `i<l` em turno, estende `k` enquanto os
símbolos casam, e registra `k` no momento da falha — ou seja,
`LCP(sufixo_i, sufixo_l)+1`; o máximo sobre todo `i` é `LPF[l]+1`; um
lema padrão de arrays de sufixos garante que, para um conjunto `S` de
sufixos, o `LCP` máximo com uma consulta é atingido por um dos dois
vizinhos imediatos em ordem de posto dentro de `S` (porque
`LCP(x,y)` para postos `r1<r2` é `min(lcp_array[r1+1..r2])`, um mínimo
de intervalo que só pode encolher ou empatar quando o intervalo cresce)
— o que justifica consultar apenas predecessor/sucessor via a árvore de
Fenwick em vez de buscar entre TODOS os `i<l`.

**A versão ingênua foi mantida** (renomeada `lz76_complexity_naive`,
nunca chamada pelo pipeline de produção) como referência confiável para
validação cruzada, não removida. `lz76_complexity` (nome público,
importado por `normalized_lzc`/`validate_synthetic.py`/todo o resto do
pipeline) agora aponta para a versão rápida.

**Validação exaustiva ANTES de integrar ao pipeline de produção** (toda
rodada ANTES de tocar dado real de novo):
- Caso de teste de Kaspar & Schuster 1987 (`c=6`): bate.
- 500 sequências aleatórias pequenas (`N<60`, alfabeto 2/3): 0
  divergências.
- 300 sequências estruturadas (constante, periódica, run-length,
  alfabeto misto, `N<400`): 0 divergências.
- `N=79.043`, alfabeto ternário, dado aleatório (tamanho EXATO do
  segmento POST-primária do Daphnet): bate (`c=7.694` em ambas as
  versões; rápida `1,03s` vs. ingênua `96,6s`).
- Segmento REAL `daphnet_pre_robust` (`N=36.472`, ambos os canais
  binário/ternário): bate (rápida `~0,4s` vs. ingênua `~17-18s`).
- Fatia decimada do segmento REAL `kilauea_pre_primary` (`N=20.000`,
  ambos os canais): bate (rápida `~0,3s` vs. ingênua `~3,4-5,6s`).
- `N=200.000` (teto de subamostragem real): `~2,4s` com a versão rápida
  (a versão ingênua nunca terminou nesse tamanho, então não há
  comparação direta de tempo, só a garantia de equivalência algorítmica
  provada acima + a validação empírica em todos os tamanhos menores).

**`validate_synthetic.py` foi reexecutado integralmente após a correção
e produziu resultados BIT-IDÊNTICOS aos já reportados nesta nota** —
`positive_control`, `negative_control`, `differential_hurst_control`,
`iaaft_power_check`, `a_priori_hypothesis_check`,
`bootstrap_fallback_check`, e `final_decision_protocol_verdict`
comparados campo a campo (exceto `wall_clock_seconds`, que naturalmente
mudou: `168,4s` no total agora vs. o tempo original) — nenhuma
divergência em nenhum campo. **Nenhuma conclusão desta nota de
validação muda.** O diagnóstico de correção de código em
`analysis/validate_synthetic.py` agora também cruza `lz76_complexity`
(rápida) contra `lz76_complexity_naive` (referência) diretamente nos 4
casos do diagnóstico (`fast_vs_naive_reference_match: true`),
tornando essa checagem visível em `validation_synthetic.json` a cada
reexecução futura, não apenas nesta nota.

Nenhuma decisão de `R_lambda`/`I(X)`/protocolo de significância foi
tocada por esta correção — é estritamente uma correção de desempenho de
implementação, com prova de equivalência matemática e validação empírica
exaustiva antes de qualquer uso em dado real. Detalhes completos do
impacto no dado real em `RESULTS_SUMMARY.md`.
