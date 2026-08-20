# Nota de validação — `homologia-persistente` (TDA via filtração de Vietoris-Rips sobre embedding de Takens), ANTES de qualquer dado real

**Status: FINAL — candidato `homologia-persistente` FECHADO NA ETAPA DE
VALIDAÇÃO.** Validação sintética obrigatória (`METHODOLOGY_NOTE.md`
Gap (c)) concluída: diagnóstico de correção de código passa limpo;
controle negativo calibra corretamente; controle positivo — o teste
central e decisivo desta candidatura — mostra `IAAFT_LOW_POWER` nos DOIS
canais (`median_max_persistence` e `median_total_persistence`); o
fallback de bootstrap por blocos móveis (Kunsch 1989), pré-autorizado em
`METHODOLOGY_NOTE.md` Gap (c) e disparado automaticamente por esta
validação, TAMBÉM não encontra poder em nenhum dos dois canais.
Pipeline (`analysis/ph_common.py`) e script de validação
(`analysis/validate_synthetic.py`) commitados; resultado completo em
`analysis/validation_synthetic.json`. **Nenhum dado real (deformação
LIGO GW150914, S&P500 ao redor da falência do Lehman Brothers) foi
tocado em nenhum momento desta linha de investigação para
`homologia-persistente`.**

## Resumo honesto do resultado

Ao contrário de `RQA` (que fechou porque o passo de embedding
COMPARTILHADO via FNN nunca resolvia para ruído branco, bloqueando
`%DET`/`ENTR` antes mesmo de poderem ser calculados), aqui o desenho
deliberado do Gap (a) — `m=3` FIXO, não FNN, `tau` recalculado
independentemente por série — funcionou exatamente como previsto: o
embedding resolveu de ponta a ponta em TODOS os controles, incluindo o
controle positivo com PRE de ruído branco puro (`0` falhas de `tau` em
`200` substitutos IAAFT do PRE e `200` do POST, em ambos os controles).
**Este NÃO é o mesmo modo de falha de `RQA`** — é um achado de PODER
genuíno, não de não-computabilidade estrutural: a estatística de
persistência de H1 foi calculada corretamente em todos os casos, mas não
separou o controle positivo do nulo IAAFT nem do nulo de bootstrap.

| Canal | `p` IAAFT (positivo) | `p` IAAFT (negativo) | `p` bootstrap (positivo) | Veredito |
|---|---|---|---|---|
| `median_max_persistence` | 0,355 | 0,645 | 0,454 | `IAAFT_LOW_POWER` (confirmado por bootstrap) |
| `median_total_persistence` | 0,320 | 0,500 | 0,368 | `IAAFT_LOW_POWER` (confirmado por bootstrap) |

Isso responde diretamente à pergunta central desta validação, nomeada em
`METHODOLOGY_NOTE.md` Gap (c): a correlação `r≈0,92` já medida na Fase
0.6 entre persistência máxima de H1 e um análogo de `%DET`(RQA), em
regime de degradação de ruído, **não era um acaso da senoide ruidosa de
brinquedo — é um sinal real de que os dois canais compartilham a mesma
falta de poder discriminante contra determinismo genuíno sob o protocolo
IAAFT**, mesmo com o `%DET`(RQA) original nunca tendo demonstrado poder
(`p=1,0` em ambos os canais, ver `../rqa/VALIDATION_NOTE.md`). A
homologia persistente HERDA a falta de poder de `%DET`, mas por um
MECANISMO DIFERENTE: RQA falhou porque o embedding compartilhado nunca
resolvia (não-computabilidade estrutural); a homologia persistente
resolve o embedding sem problema algum (graças ao `m=3` fixo,
deliberadamente desenhado para evitar exatamente esse problema), mas a
estatística de persistência em si — mesmo bem calibrada e corretamente
computada — simplesmente não separa determinismo caótico genuíno do
nulo IAAFT/bootstrap neste desenho.

## Diagnóstico de correção de código (ANTES dos controles estocásticos)

Rodado primeiro, como exigido pela tarefa: onda senoidal determinística
(período 50, N=1.000) com um dither Gaussiano relativo de `1e-6`
(precaução padrão desta linha, embora o critério de razão do FNN que
motivou o dither em RQA/`kramers_moyal` não se aplique aqui — `ripser`
não tem o mesmo modo de falha de denominador quase-zero).

- `tau=5` (mínimo local de MI), `M=990` pontos embedded (`m=3` fixo),
  `4` sub-janelas de `N_WINDOW=200` (o teto de `K_SUBWINDOWS_MAX=10` não
  é atingido com `N=1.000`).
- `median_max_persistence=1,4763`, `median_total_persistence=1,4807` —
  valor grande e inequívoco, consistente com um laço fechado claro no
  espaço de fase de uma senoide pura embedded com `m=3`.
- As `4` sub-janelas dão valores de `max_persistence` quase idênticos
  (`1,476306 / 1,476305 / 1,476305 / 1,476303`) — variação de
  `~3×10⁻⁶`, exatamente a escala do dither, confirmando que o código
  detecta consistentemente o MESMO laço geométrico em cada sub-janela de
  uma dinâmica estacionária, e que o `median` sobre sub-janelas é uma
  agregação estável.

**Confirma que o código de embedding + seleção de sub-janelas + Rips +
extração de persistência de H1 está correto** antes de testar em dado
genuinamente ambíguo. `0,155s` de tempo de parede para este diagnóstico.

## Controles sintéticos (`N=3.000`, `seed=12345`, `N_SURROGATES=200`, `N_IAAFT_ITER=50`)

### Controle negativo (dois sorteios independentes de fGn-like, H=0,7 fixo)

PRE e POST = duas realizações INDEPENDENTES do mesmo processo fGn-like
(gerador de síntese espectral, `H=0,7` fixo, seeds 555001/555002).
`tau` resolvido independentemente por série (PRE=83, POST=73 — variação
esperada entre realizações independentes de um processo colorido),
`M_PRE=2.834`, `M_POST=2.854`, `10` sub-janelas usadas em ambos.

| Canal | PRE real | POST real | `Δ` real | nula IAAFT (média±dp) | `p` (bicaudal) | veredito |
|---|---|---|---|---|---|---|
| `median_max_persistence` | 0,05905 | 0,05328 | −0,00576 | 0,00098 ± 0,01396 | **0,645** | corretamente não significativo |
| `median_total_persistence` | 0,21991 | 0,19333 | −0,02658 | −0,01436 ± 0,04054 | **0,500** | corretamente não significativo |

`n=200` substitutos IAAFT válidos em ambos os canais (nenhuma falha de
`tau` ou amostra insuficiente entre os 400 substitutos gerados, PRE+POST).
`165,2s` de tempo de parede.

### Controle positivo — o teste central e decisivo (`METHODOLOGY_NOTE.md` Gap (c), especificação exata)

PRE = ruído branco Gaussiano iid (`N=3.000`, seed 424242). POST = mapa
logístico caótico (`r=4`), remapeado por posto (rank-remap) sobre os
valores exatos do PRE — marginal idêntica por construção. Espectro
confirmado empiricamente quase plano em ambos
(`spectral_exponent_pre=−0,058`, `spectral_exponent_post=+0,014`), sem o
descasamento espectral que fechou a v1 do controle positivo de `RQA`
(lá o problema nunca chegou a este ponto porque o embedding nem
resolvia).

**Embedding resolveu sem problema em ambos:** `tau_PRE=2`, `tau_POST=12`
(mínimo local de MI, `status=ok`, `m=3` fixo em ambos por desenho),
`M_PRE=2.996`, `M_POST=2.976`, `10` sub-janelas usadas em cada um — `0`
falhas de `tau` entre os `400` substitutos IAAFT gerados (200 PRE + 200
POST). Isso confirma diretamente que o Gap (a) cumpriu seu objetivo:
ruído branco puro como PRE NÃO bloqueia este pipeline, ao contrário do
que aconteceu com a regra de FNN de RQA.

| Canal | PRE real | POST real | `Δ` real | nula IAAFT (média±dp) | `p` (bicaudal) | sigma-equivalente | veredito |
|---|---|---|---|---|---|---|---|
| `median_max_persistence` | 0,40732 | 0,37919 | −0,02813 | 0,00057 ± 0,03379 | **0,355** | **−0,85σ** | `IAAFT_LOW_POWER` |
| `median_total_persistence` | 8,41348 | 8,91998 | +0,50650 | 0,00949 ± 0,50319 | **0,320** | **+0,99σ** | `IAAFT_LOW_POWER` |

`124,7s` de tempo de parede para esta chamada completa de
`run_ph_analysis` (`N=3.000`, `N_SURROGATES=200`) — ver seção de custo
computacional abaixo.

**Nenhum dos dois `p`-valores chega perto de `0,05`** (`0,355` e
`0,320`), e os sigma-equivalentes (`−0,85σ`, `+0,99σ`) são pequenos em
magnitude absoluta — diferente do achado de `RQA` v2 (Rössler), onde
sigma-equivalentes grandes (`8,94σ`, `2,81σ`) coexistiam com `p=1,0` por
um motivo estrutural específico (nula estreita e deslocada). Aqui a nula
IAAFT é razoavelmente larga e centrada perto de zero, e o `Δ` real cai
dentro dela sem folga — um achado de poder baixo mais direto e menos
sutil que o de RQA.

**Hipótese investigada, não decidida:** um candidato mecanístico
honesto para por que o sinal não aparece, sem provar definitivamente:
ruído branco puro embedded com `m=3` já produz uma nuvem de pontos
difusa com um piso de "ruído geométrico" substancial — `median_max_
persistence` do PRE (ruído puro) é `0,407`, quase **7x maior** que o
`median_max_persistence` do PRE do controle negativo (fGn H=0,7,
`0,059`). Ruído branco, sem nenhuma autocorrelação, gera laços aleatórios
espúrios na nuvem de pontos embedded simplesmente por acaso geométrico
(qualquer configuração densa e desestruturada de pontos tem ALGUMA
persistência de H1 não-trivial). Esse piso de ruído geométrico pode estar
grande o bastante para mascarar o sinal topológico genuíno introduzido
pela dinâmica de baixa dimensão do mapa logístico — hipótese consistente
com, mas não provada por, os números acima (não investigada mais a fundo
porque não muda o veredito de poder, que já é decisivo pelo critério
pré-declarado de `p`-valor).

## Fallback de bootstrap por blocos móveis (Kunsch 1989) — pré-autorizado, disparado automaticamente, TAMBÉM não resolve

`METHODOLOGY_NOTE.md` Gap (c) pré-autoriza bootstrap por blocos móveis
como teste PRIMÁRIO complementar "se a validação mostrar baixo poder
(mesmo padrão de DFA-alpha)" — disparado aqui automaticamente pelo
próprio `validate_synthetic.py` assim que os dois canais do controle
positivo vieram `IAAFT_LOW_POWER`, não decidido manualmente depois de ver
o resultado.

Reamostragem de blocos móveis do MESMO controle positivo (ruído branco
PRE / mapa logístico remapeado POST), comprimento de bloco
`L=max(2×mediana(tau_PRE,tau_POST), 10)=14` amostras, `n_bootstrap=1.000`
por segmento:

| Canal | `Δ` real | nula bootstrap (média±dp) | `p` bootstrap (bicaudal) | veredito |
|---|---|---|---|---|
| `median_max_persistence` | −0,02813 | −0,00362 ± 0,03533 | **0,454** | não significativo |
| `median_total_persistence` | +0,50650 | +0,14333 ± 0,55151 | **0,368** | não significativo |

`n=1.000` reamostras válidas em ambos os canais (nenhuma falha de `tau`
ou amostra insuficiente). `574,3s` de tempo de parede para este teste
(mais caro que o IAAFT porque `n_bootstrap=1.000` > `N_SURROGATES=200`).

**Isso descarta uma miscalibração específica do IAAFT como explicação
completa** — trocar o teste de significância para um método
completamente diferente (bootstrap de blocos, que não depende da
suposição de processo gaussiano-linear-com-mesmo-espectro do IAAFT) não
muda o veredito: nenhum dos dois canais mostra significância sob nenhum
dos dois testes.

## Custo computacional — medido, não estimado, dentro do orçamento previsto

| Item | Tempo de parede |
|---|---|
| Diagnóstico de correção de código (`N=1.000`, sem substitutos) | 0,155s |
| Uma chamada completa de `run_ph_analysis` (`N=3.000`, `N_SURROGATES=200`, controle positivo) | **124,7s (~2,1 min)** |
| Controle negativo completo (`N=3.000`, `N_SURROGATES=200`) | 165,2s |
| Fallback de bootstrap (`n_bootstrap=1.000` × 2 canais, controle positivo) | 574,3s (~9,6 min) |
| **Total do script de validação** | **864,4s (~14,4 min)** |

Consistente com a estimativa a priori de `METHODOLOGY_NOTE.md` Gap (e)
("dezenas de minutos, mesma ordem de grandeza de VG/RQA"). Uma única
chamada de `run_ph_analysis` no protocolo completo de 200 substitutos
custa ~2 minutos para `N=3.000` — bem dentro do orçamento medido na Fase
0.6 (3.240 pontos = 16,4s POR DIAGRAMA single-core; aqui cada diagrama
individual opera sobre apenas `N_WINDOW=200` pontos, ~0,15-0,2s cada,
e o desenho de sub-janelas do Gap (b) é exatamente o que mantém isso
tratável). **Implicação para o passo de dado real:** mesmo com segmentos
reais potencialmente maiores (LIGO: até 32s × 4096Hz; S&P500: histórico
diário completo), o custo é limitado pelo desenho `K_SUBWINDOWS_MAX=10`
× `N_WINDOW=200`, não pelo tamanho bruto do segmento — o custo de uma
chamada completa NÃO deveria crescer proporcionalmente ao tamanho do
segmento real além do necessário para estimar `tau` (barato, O(N) por
lag) e para selecionar as sub-janelas (também barato). Se este candidato
tivesse passado na validação, o passo de dado real seria tratável em
minutos, não horas.

## Nenhum desvio metodológico não declarado

Toda decisão de implementação seguiu `METHODOLOGY_NOTE.md` literalmente:
`m=3` fixo (Gap a), `tau` via mínimo local de MI recalculado por série
com fallback de cruzamento por zero da ACF (Gap a), desenho de
sub-janelas `N_WINDOW=200`/`K_SUBWINDOWS_MAX=10` evenly-spaced cobrindo
o segmento inteiro (Gap b, ver docstring de `select_subwindow_starts` em
`ph_common.py` para a prova de que o stride escolhido garante
simultaneamente não-sobreposição e cobertura total), `I(X)` primário e
companheiro exatamente como especificados (Gap b), protocolo IAAFT
completo com `tau` recalculado por substituto (Gap e), bootstrap de
blocos móveis pré-autorizado disparado automaticamente pelo mesmo
critério de baixo poder já usado em RQA/`kramers_moyal` (Gap c). Único
detalhe de implementação não discutido explicitamente pelo texto da nota
de metodologia, documentado aqui e no docstring de
`h1_persistence_stats`: features H1 com morte não-finita (classe
essencial) seriam excluídas de ambas as estatísticas caso aparecessem —
não ocorreram em nenhum diagrama computado nesta validação (`ripser`
com `maxdim=1` sobre nuvens finitas de 200 pontos não produziu nenhuma
classe H1 essencial em nenhum dos milhares de diagramas calculados).

## Veredito — aplicado honestamente, sem forçar, decisão de fechamento confirmada pela sessão orquestradora

Per revisão direta da sessão orquestradora sobre os resultados completos
de `validation_synthetic.json` (não decidido unilateralmente por este
agente): **os dois canais mostraram `IAAFT_LOW_POWER` no controle
positivo — o teste central e decisivo desta validação — E o único
fallback pré-autorizado por `METHODOLOGY_NOTE.md` Gap (c) para esse
padrão (bootstrap por blocos móveis, Kunsch 1989) TAMBÉM não encontra
poder em nenhum dos dois canais.** Nenhuma terceira tentativa de
redesenho (ex. controle positivo dedicado com outro sistema caótico,
como o Rössler usado no addendum de RQA) foi pré-autorizada por
`METHODOLOGY_NOTE.md` para este candidato, e — seguindo a mesma
disciplina de "nenhum ajuste aberto/aberto-ended tuning" já aplicada a
RQA e ao canal `beta_D2` de `kramers_moyal` — nenhuma foi tentada aqui.

> **O candidato `homologia-persistente` é FECHADO NA ETAPA DE VALIDAÇÃO
> — nem `median_max_persistence` nem `median_total_persistence` de H1
> mostraram poder discriminante real contra o nulo IAAFT ou contra o
> nulo de bootstrap de blocos móveis, no único desenho de controle
> positivo especificado a priori em `METHODOLOGY_NOTE.md` Gap (c)
> (PRE=ruído branco, POST=mapa logístico `r=4` remapeado por posto).
> Nenhum dado real (deformação LIGO GW150914, S&P500 ao redor da
> falência do Lehman Brothers) foi tocado em nenhum momento desta linha
> de investigação para `homologia-persistente`. Isso confirma
> empiricamente — não apenas por analogia teórica — que o risco de
> identificabilidade nomeado em `METHODOLOGY_NOTE.md` Gap (c) (a
> correlação `r≈0,92` entre persistência máxima de H1 e um análogo de
> `%DET`(RQA), já medida na checagem informal da Fase 0.6 em senoide
> ruidosa) era um sinal real e substantivo de risco compartilhado, não
> uma coincidência do exemplo de brinquedo daquela checagem. A homologia
> persistente, PELO MENOS neste desenho (`m=3` fixo, sub-janelas de
> `N_WINDOW=200`, mediana de persistência máxima/total de H1 sobre até
> 10 sub-janelas), HERDA a falta de poder discriminante que `%DET`(RQA)
> já havia demonstrado (`p=1,0` em ambos os canais, controle positivo
> Rössler) — mas por um MECANISMO DIFERENTE: RQA falhou porque o
> embedding compartilhado via FNN nunca resolvia para ruído branco
> (não-computabilidade estrutural, `%DET`/`ENTR` nunca puderam sequer
> ser calculados); a homologia persistente resolve o embedding sem
> nenhum problema (o `m=3` fixo do Gap (a) cumpriu exatamente seu
> objetivo de evitar a parede de FNN de RQA), mas a estatística de
> persistência em si — corretamente computada, corretamente calibrada
> no controle negativo — simplesmente não separa determinismo caótico
> genuíno do nulo sob nenhum dos dois testes de significância tentados.
> Este é um resultado válido, honesto e completo — "poder não
> estabelecido na validação sintética, por dois testes de significância
> independentes" —, não um resultado parcial, abandonado, ou uma falha
> a esconder.**

Com este fechamento, os **11 candidatos** identificados ao longo de toda
a busca da linha `DISC-TRI-RG-001` têm veredito final: os candidatos
testados em dado real que não sobreviveram, mais `RQA` (fechado na etapa
de validação, embedding não-computável) e agora `homologia-persistente`
(fechado na etapa de validação, poder estatístico não estabelecido) —
nenhum candidato desta linha produziu um invariante cross-domain
sobrevivente até o momento. Registro de `RESULTS_SUMMARY.md`,
`TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md`, incluindo a síntese de toda
a rodada de busca da Fase 0.6, fica a cargo da sessão orquestradora,
conforme ela mesma indicou.
