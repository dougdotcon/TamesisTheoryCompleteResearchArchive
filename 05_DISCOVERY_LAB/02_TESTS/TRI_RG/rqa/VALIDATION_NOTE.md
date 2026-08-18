# Nota de validação — `RQA` (Análise de Quantificação de Recorrência), ANTES de qualquer dado real

**Status: FINAL — candidato `RQA` FECHADO NA ETAPA DE VALIDAÇÃO.** Validação
sintética obrigatória (`METHODOLOGY_NOTE.md` Gap (b), mais o adendo do Gap
(b) redesenhado, commit `024e7a9`) concluída em DUAS tentativas de controle
positivo pré-autorizadas (mapa logístico, depois Rössler) — nenhuma
estabeleceu poder real do IAAFT em `%DET`/`ENTR`. Ver "Veredito FINAL" no
Adendo abaixo para o resultado decisivo. Pipeline (`analysis/rqa_common.py`)
e script de validação (`analysis/validate_synthetic.py`) commitados;
resultado completo em `analysis/validation_synthetic.json`. **Nenhum dado
real foi tocado em nenhum momento desta linha de investigação para `RQA`.**

## Resumo honesto do resultado

A validação encontrou um achado estrutural — não um problema de poder do
IAAFT — mais fundamental ainda do que o de `grafo-de-visibilidade`, porque
aqui ele bloqueia os **dois canais simultaneamente**, não apenas um:

**O controle positivo, exatamente como especificado em `METHODOLOGY_NOTE.md`
Gap (b) (PRE = ruído branco Gaussiano iid), não pôde ser calculado.** A
etapa de embedding COMPARTILHADA (`(m,tau)` estimado uma única vez a partir
do PRE, Gap (a)) falha antes mesmo de `%DET`/`ENTR` poderem ser computados:
Falsos Vizinhos Mais Próximos (FNN, Kennel, Brown & Abarbanel 1992,
`R_tol=10`, `A_tol=2`) nunca cai abaixo do limiar de 1% para nenhum `m` em
`1..10` quando aplicado a ruído branco iid puro. Como `(m,tau)` é
compartilhado entre `%DET` e `ENTR`, essa falha bloqueia AMBOS os canais ao
mesmo tempo — diferente do achado de `grafo-de-visibilidade`, onde `d_B`
falhava mas `C` continuava computável.

## Achado estrutural (descoberto POR esta validação, testado explicitamente, não assumido)

Ruído branco genuíno (autocorrelação zero, "flat" em qualquer dimensão) é o
pior caso possível para FNN: sem estrutura de correlação temporal alguma,
não existe um `m` finito que "resolva" a dinâmica — cada dimensão adicional
apenas reamostra ruído independente, então a fração de falsos vizinhos nunca
converge para perto de zero. Isso é teoricamente esperado (mencionado no
próprio artigo original de Kennel et al. 1992: ruído puro nunca atinge FNN
baixo em dimensão finita) e foi confirmado empiricamente aqui de forma
robusta:

| Verificação | Resultado |
|---|---|
| Ruído branco Gaussiano, N=2.000, 5 seeds distintas | 0/5 resolveu `m<=10`; fração mínima de FNN atingida entre 17,3%–20,3% (m~4-5), volta a subir depois (17-40%+ em m=10) |
| Ruído branco Gaussiano vs. uniforme, N=2.000 | ambos falham igualmente — não é peculiaridade da marginal Gaussiana |
| N=2.000 vs. N=5.000 (teto do Gap (d)), 2 seeds cada | falha idêntica em todos — **mais dado não ajuda**, é independente de `N` dentro do teto de subamostragem |
| Varredura fGn-like, H fixo, N=2.000 | H=0,1: falha. H=0,3 a H=0,9: resolve (`m` entre 3 e 8) — fronteira de resolubilidade fica perto de H~0,2–0,3 |
| Varredura AR(1), φ fixo, N=2.000 | φ=0,0 a φ=0,9: falha. φ=0,95: resolve (`m=7`) — só resolve quando a autocorrelação é MUITO forte |

Conclusão da caracterização: a exigência do Gap (b) por um PRE "ruído
branco" — necessária ali precisamente para casar espectro+marginal com o
mapa logístico via *rank-remap* sem confundir o teste com uma diferença
espectral não controlada (ver seção "Por que não foi usado outro PRE" abaixo)
— cai exatamente na região onde FNN estruturalmente não converge sob os
parâmetros travados a priori (`R_tol=10`, `A_tol=2`, `m<=10`).

## Diagnóstico de correção do código (ANTES dos controles estocásticos)

Rodado primeiro, como exigido pela tarefa: onda senoidal determinística
(período 50, N=1.000) com um pequeno "dither" (ruído Gaussiano de amplitude
relativa `1e-6`). O dither foi necessário e é documentado explicitamente: uma
senoide perfeitamente periódica em ponto flutuante produz muitos pontos de
embedding coincidentes até a precisão de máquina (o período 50 se repete
exatamente a cada ciclo, 20 ciclos em N=1.000), o que faz o critério de razão
do FNN (`|diff|/R_i^m > R_tol`) explodir sobre denominadores da ordem de
`1e-16` — ruído numérico de divisão quase-por-zero, não um sinal dinâmico
real. Um dither de `1e-6` quebra essas coincidências exatas sem alterar a
dinâmica genuína (nem a verdadeira dimensão pequena do atrator, `m=2`
teoricamente para uma senoide pura).

Resultado: `tau=5` (mínimo local de MI), `m=4` resolvido por FNN (fração cai
de 55% em m=1 até 0,6% em m=8 nos testes preliminares; no diagnóstico final
`m=4` já suficiente com N=1.000), `%DET=0,9994` (muito próximo de 1,0, como
esperado para dinâmica puramente determinística), `ENTR=1,487`,
`RR` atingida `=0,050005` (bate com `RR_target=0,05`). **Confirma que o
código de embedding + matriz de recorrência + `%DET`/`ENTR` está correto**
antes de testar em dado genuinamente ambíguo.

## Controles sintéticos (N=2.000, `seed=12345`, `N_SURROGATES=200`)

### Controle positivo (`METHODOLOGY_NOTE.md` Gap (b), especificação exata)

PRE = ruído branco Gaussiano iid. POST = mapa logístico caótico (`r=4`),
remapeado por posto (rank-remap) sobre os valores exatos do PRE — marginal
idêntica por construção, espectro confirmado empiricamente quase plano em
ambos (`spectral_exponent_pre=-0,027`, `spectral_exponent_post=+0,022`).

| Canal | Resultado |
|---|---|
| `tau` (PRE) | `2` (mínimo local de MI, `status=ok`) |
| `m` (PRE, FNN) | **NÃO RESOLVIDO** — fração mínima de FNN = 17,9% em `m=4`, nunca cai abaixo de 1% até `m=10` (curva completa: 99,6% / 74,8% / 29,4% / 17,9% / 18,5% / 21,7% / 24,6% / 31,4% / 40,8% / 53,1%) |
| `%DET`, `ENTR` | **indefinidos** — embedding compartilhado nunca fixado, nada pôde ser calculado para PRE nem POST |
| `p_DET`, `p_ENTR` | **indefinidos** (não "não significativo" — nenhum valor real ou nulo IAAFT pôde ser formado) |

### Controle negativo (dois sorteios independentes de fGn-like, H=0,7 fixo)

Sonda diretamente o risco espectral/linear nomeado no Gap (b) — e, ao
contrário do ruído branco, ESTE processo resolve o embedding (H=0,7 fica bem
dentro da região resolúvel da varredura acima), permitindo exercitar o
pipeline completo (embedding + recorrência + IAAFT) de ponta a ponta.

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | p (bicaudal) | veredito |
|---|---|---|---|---|---|---|---|
| `%DET` (`m=4`,`tau=49`) | 0,98239 | 0,98503 | +0,002644 | 0,005113 | 0,003973 | **0,77** | corretamente não significativo |
| `ENTR` | 3,41275 | 3,49238 | +0,079630 | 0,130494 | 0,174997 | **0,70** | corretamente não significativo |

`n=200` substitutos IAAFT válidos em ambos os canais (nenhum indefinido).

## Teste do fallback de bootstrap (pré-autorizado, testado empiricamente, não assumido)

`METHODOLOGY_NOTE.md` Gap (e) pré-autoriza bootstrap por blocos móveis
(Kunsch 1989) como teste PRIMÁRIO complementar **se a validação repetir o
padrão de baixo poder já visto em DFA-alpha**. A máquina de bootstrap
(`run_block_bootstrap_test`, `moving_block_bootstrap_resample`) já está em
`rqa_common.py`. Testado diretamente aqui, não assumido, per instrução da
tarefa: **25 reamostras de blocos móveis (comprimento de bloco `L=20`) do
mesmo segmento de ruído branco usado no controle positivo — 0/25 resolveram
o embedding (`m<=10`)**, com `tau` variando entre reamostras (2 a 8) mas
`m_status="embedding_not_resolved"` em todas. Isso confirma diretamente,
sem precisar assumir por analogia com `grafo-de-visibilidade`: reamostrar
blocos de uma série SEM autocorrelação (ruído branco) produz outra série sem
autocorrelação — a propriedade estrutural que quebra FNN não é sensível a
reordenação por blocos, então o bootstrap não pode ajudar aqui, exatamente
como não ajudou o `d_B` de `grafo-de-visibilidade` (por um motivo distinto
lá — topologia de grafo pequeno-mundo — mas com a mesma conclusão prática:
bootstrap corrige PODER estatístico, não NÃO-COMPUTABILIDADE estrutural).

## Por que não foi usado outro PRE para "salvar" o controle positivo

Foi considerado, apenas como checagem de curiosidade (NÃO oferecido como
substituto do Gap (b), e não incluído formalmente em
`validation_synthetic.json`): usar PRE = fGn-like H=0,7 (que resolve FNN) e
POST = mapa logístico remapeado por posto sobre ESSE PRE, no lugar de ruído
branco. Resultado dessa checagem informal: `Δ_DET=-0,775`, mas a média nula
IAAFT ficou em `-0,880` (desvio `0,0035`) — ou seja, o Δ real ficou MENOS
extremo que a média dos substitutos, `p_DET=1,0`. Isso NÃO é evidência de
ausência de determinismo genuíno; é confusão experimental: o mapa logístico
bruto tem espectro naturalmente quase-branco/de banda larga, então remapeá-lo
por posto sobre a marginal de um fGn H=0,7 (espectro fortemente colorido)
NÃO produz o casamento de espectro que o Gap (b) exige — cria um
descasamento espectral não controlado entre PRE e POST, que o IAAFT
(que preserva o espectro de CADA série) reproduz corretamente, mascarando
qualquer sinal de determinismo não-linear genuíno. Isso é precisamente por
que `METHODOLOGY_NOTE.md` especifica ruído branco como PRE do controle
positivo: é a forma mais simples de obter PRE e POST com espectros
naturalmente casados (ambos banda larga) via *rank-remap*. Trocar o PRE por
outro processo para "contornar" a falha de FNN reintroduziria exatamente o
confundidor espectral que o desenho original evita — não é uma correção
válida, e não foi adotada. Reportado aqui apenas como contexto, não como
resultado formal.

## Veredito de validação — honesto, sem forçar, sem decidir unilateralmente o próximo passo

- **`%DET` (canal primário) e `ENTR` (canal companheiro):**
  `NOT_COMPUTABLE_EMBEDDING_NOT_RESOLVED` para AMBOS, especificamente para o
  controle positivo tal como especificado no Gap (b) (`PRE`=ruído branco).
  Isso é DIFERENTE de "sem sinal" ou "baixo poder" — nenhum valor real de
  `%DET`/`ENTR` pôde sequer ser calculado para o PRE do controle positivo,
  então nenhum p-valor pôde ser formado. O controle negativo (fGn H=0,7,
  processo com autocorrelação genuína) resolve o embedding normalmente e
  produz `p` corretamente não-significativo em ambos os canais — confirma
  que o pipeline funciona corretamente quando a etapa de embedding é
  computável, isolando o problema à combinação específica "ruído branco
  puro como PRE" + "FNN com os parâmetros travados a priori".
- **Bootstrap:** testado explicitamente, não resolve (0/25 reamostras do
  controle positivo resolveram o embedding) — confirma que este NÃO é o
  padrão de baixo poder do DFA-alpha, é o mesmo tipo de parede estrutural já
  visto (por outro mecanismo) no `d_B` de `grafo-de-visibilidade`.

**Nenhum desvio metodológico foi feito além do que o próprio
`METHODOLOGY_NOTE.md` já pré-autorizava** (a máquina de bootstrap foi
adicionada e testada, exatamente como o Gap (e) previa como possibilidade) —
as regras de `tau`, `m`, `epsilon`, janela de Theiler, `RR_target`,
`MAX_N_PER_SEGMENT`, e o protocolo IAAFT permanecem exatamente como
fixados, sem reformulação alguma depois de ver o resultado. Em particular:
**este agente NÃO decidiu retirar `%DET` ou `ENTR` do critério de decisão**
— essa é uma decisão de governança que, por instrução explícita da tarefa,
cabe à sessão orquestradora, não a este agente dispatchado. O achado fica
registrado aqui para essa decisão.

## Adendo — segunda tentativa de controle positivo (Rössler), decisiva, FINAL

Após a sessão orquestradora revisar o achado acima, a metodologia foi
corrigida em `METHODOLOGY_NOTE.md` (commit `024e7a9`, adendo "controle
positivo do Gap (b) redesenhado"): trocar a fonte do sinal caótico de POST
do mapa logístico (espectro banda-larga/quase-branco, causa do confundidor
espectral já documentado acima) para o **sistema de Rössler** (Rössler
1976, `a=0,2, b=0,2, c=5,7`, regime caótico clássico, integração RK4 com
passo interno `dt_internal=0,01`, reamostrado em `dt=0,15`), mantendo
PRE=fGn-like `H=0,7` (já validado, resolve FNN) e a mesma técnica de
remapeamento por posto. Protocolo de decisão fixado a priori: se `%DET`
e/ou `ENTR` mostrarem poder real (`p<0,05`), validação passa; se nenhum dos
dois mostrar, `RQA` é fechado na etapa de validação — **nenhuma terceira
tentativa autorizada**, de qualquer forma.

### Casamento espectral (reportado honestamente, sem exigir perfeição)

`dt=0,15` foi escolhido especificamente por dar um expoente espectral (via
inclinação de periodograma) para a trajetória Rössler bruta de `2,397` —
muito próximo do expoente-alvo do fGn H=0,7 (`2*0,7+1=2,4`). Após o
remapeamento por posto sobre a marginal do PRE:

| Série | Expoente espectral |
|---|---|
| PRE (fGn H=0,7) | 2,3726 |
| Rössler bruto (antes do remap) | 2,3968 |
| POST (Rössler remapeado sobre PRE) | 1,9583 |

Casamento bom mas não perfeito — o remapeamento por posto, sendo uma
transformação monótona não-linear, não preserva exatamente o formato
espectral da série bruta (esperado, mesmo padrão já visto no controle
positivo v1). Ainda assim, muito mais próximo do PRE do que o mapa
logístico jamais esteve (v1: PRE quase-plano `-0,027`, POST quase-plano
`+0,022` — mas contra um PRE de ruído branco que nem resolvia o embedding).

### Resultado — embedding RESOLVE desta vez (confirma que a correção de desenho funcionou nesse nível)

| | Valor |
|---|---|
| `tau` (PRE) | 40 |
| `m` (PRE, FNN) | 4 (`status=ok`) |
| `%DET` PRE / POST / Δ | 0,98298 / 0,93488 / **−0,04810** |
| `ENTR` PRE / POST / Δ | 3,40309 / 2,22523 / **−1,17787** |
| média nula IAAFT (`%DET`) | −0,11526 (desvio 0,00751) |
| média nula IAAFT (`ENTR`) | −1,51536 (desvio 0,12021) |
| `p_DET` (bicaudal, `n=200`) | **1,0** |
| `p_ENTR` (bicaudal, `n=200`) | **1,0** |
| desvios-padrão equivalentes | `%DET`: ≈8,94σ · `ENTR`: ≈2,81σ (ver nota abaixo — NÃO indicam significância) |

**Resultado decisivo: `p=1,0` em AMBOS os canais.** Não é apenas "não
atingiu o limiar de 0,05" — é o valor de p bicaudal mais alto possível,
porque o Δ real tem magnitude MENOR que a de praticamente todos os 200
substitutos IAAFT (`|Δ_real|` menor que quase todo `|Δ_substituto|`), então
a fração de substitutos com `|Δ_substituto| >= |Δ_real|` é ~100%.

**Nota honesta sobre os desvios-padrão equivalentes aparentemente grandes
(8,94σ / 2,81σ) apesar de `p=1,0`:** isso não é uma contradição, é uma
consequência de a distribuição nula IAAFT ser muito estreita (desvio
`0,0075` para `%DET`) e centrada bem longe de zero (`-0,115`), enquanto o Δ
real fica entre a nula e zero — ou seja, o Δ real é MENOS extremo (mais
próximo de "nenhuma mudança") que o Δ típico já produzido só pela diferença
de espectro entre PRE e POST que o IAAFT reproduz. O critério de decisão
pré-declarado é o valor-p bicaudal por MAGNITUDE (`|Δ_substituto|>=|Δ_real|`),
não a distância à média nula — e por esse critério, correto e fixado a
priori, o resultado é inequivocamente não significativo em ambos os canais.
Não foi investigado mais a fundo (ex. se isso reflete alguma propriedade
mais profunda de como o remapeamento por posto do Rössler interage com o
IAAFT) porque o valor-p, não o sigma-equivalente, é o critério de decisão
pré-declarado, e ele já é decisivo.

### Veredito FINAL — aplicado mecanicamente, sem desvio

Per `METHODOLOGY_NOTE.md` adendo (commit `024e7a9`), passo 5: **nenhum dos
dois canais mostrou poder real sob o segundo desenho** (`p_DET=1,0`,
`p_ENTR=1,0`, ambos `IAAFT_LOW_POWER`). Portanto:

> **O candidato `RQA` é FECHADO NA ETAPA DE VALIDAÇÃO — a identificabilidade
> de `%DET`/`ENTR` sob a convenção de embedding travada (`R_tol=10`,
> `A_tol=2`, `m<=10`, `RR_target=0,05`) não pôde ser estabelecida com
> NENHUM dos dois desenhos de controle positivo tentados (mapa logístico
> nem Rössler). Nenhum dado real (rolamento IMS/Rexnord, sismologia
> vulcânica de Kīlauea 2018) foi tocado em nenhum momento desta linha de
> investigação para `RQA`. Este é um resultado válido, honesto e completo
> — "identificabilidade não estabelecida na validação sintética" —, não um
> resultado parcial, abandonado, ou uma falha a esconder. Nenhuma terceira
> tentativa de redesenho foi feita, conforme pré-autorizado e travado ANTES
> de ver este resultado.**

Com isso, os 7 candidatos identificados para `DISC-TRI-RG-001` têm veredito
final: 6 testados em dado real e NEGATIVOS (`critical_slowing_down`,
`wavelet_multiresolution`, `dfa_multiscale_entropy`, `soc_avalanches`,
`mse_multiscale_entropy`, `visibility_graph`); `RQA` (7º e último) fechado
na etapa de validação sintética, sem nunca alcançar dado real. Registro de
`RESULTS_SUMMARY.md`, `TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` para esta
linha fica a cargo da sessão orquestradora.

## [SUPERADO PELO ADENDO ACIMA] O que se cogitou para o próximo passo, antes da segunda tentativa

A seção abaixo foi escrita ANTES da segunda tentativa de controle positivo
(Rössler, ver "Adendo" acima) e refletia a situação intermediária em que
apenas o controle positivo v1 (mapa logístico) tinha sido tentado. Mantida
aqui, riscada logicamente mas não apagada, por transparência do raciocínio
em cada etapa — **não reflete mais o estado final**. O estado final é o
veredito do Adendo: `RQA` fechado na etapa de validação, dado real nunca
tocado, nenhuma decisão pendente sobre prosseguir ou não — a decisão já foi
tomada (não prosseguir) pela própria regra de decisão pré-declarada.

Texto original (contexto histórico apenas):

> Quando (em um passo futuro e separado) `run_rqa_analysis` for aplicado aos
> 2 domínios reais (rolamento IMS/Rexnord, sismologia vulcânica de Kīlauea
> 2018), a expectativa honesta, já declarada aqui ANTES de ver qualquer dado
> real, é:
>
> - Segmentos PRE reais que se pareçam com ruído de fundo pouco estruturado
>   (ex. vibração de rolamento saudável, tremor sísmico de fundo antes de
>   qualquer atividade) correm risco real de cair na mesma zona de
>   `embedding_not_resolved` que o ruído branco sintético caiu aqui — isso
>   DEVE ser reportado honestamente como tal (não como "%DET/ENTR não
>   mudaram" nem qualquer alegação de ausência de sinal), exatamente como
>   `run_rqa_analysis` já retorna `status="embedding_not_resolved"` de forma
>   explícita e não silenciosa para esse caso.
> - Segmentos PRE reais com autocorrelação mais forte (mais prováveis em
>   dados mecânicos/sismológicos reais, que tipicamente têm conteúdo espectral
>   não-branco — ressonâncias mecânicas, microssismicidade de banda limitada)
>   têm chance real de resolver o embedding normalmente, caso em que o
>   protocolo IAAFT validado aqui (poder confirmado no controle negativo,
>   ainda que não no controle positivo por razões estruturais, não de poder)
>   pode ser aplicado como especificado.
> - **Decisão pendente para a sessão orquestradora, não tomada aqui:** dado
>   que o controle positivo do Gap (b) não pôde ser executado como
>   especificado, não há confirmação empírica de que o par `%DET`/`ENTR`
>   responde a determinismo não-linear genuíno além do que IAAFT reproduziria
>   — apenas confirmação de que, QUANDO o embedding É computável, o pipeline
>   produz p-valores corretamente calibrados sob a hipótese nula (controle
>   negativo). Se e como prosseguir para o dado real dado esse gap de
>   validação de poder fica para a sessão orquestradora decidir, não para este
>   agente.

Essa decisão pendente foi resolvida pelo Adendo: a segunda tentativa
(Rössler) também não mostrou poder real em nenhum canal, então — pela regra
fixada a priori — não há um "próximo passo de dado real" para `RQA` nesta
rodada. Ver "Veredito FINAL" no Adendo acima.
