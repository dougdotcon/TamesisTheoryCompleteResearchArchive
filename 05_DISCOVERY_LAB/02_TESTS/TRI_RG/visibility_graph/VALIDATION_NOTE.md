# Nota de validação — `grafo-de-visibilidade`, ANTES de qualquer dado real

**Status:** validação sintética obrigatória (`METHODOLOGY_NOTE.md` Gap (b))
concluída. Pipeline (`analysis/vg_common.py`) e script de validação
(`analysis/validate_synthetic.py`) commitados; resultado completo em
`analysis/validation_synthetic.json`. Nenhum dado real foi tocado.

## Resumo honesto do resultado

A validação encontrou um resultado **misto e assimétrico entre os dois
canais**, mais fundamental do que o padrão de baixo poder já visto em
`dfa-multiscale-entropy` — não é escondido nem suavizado aqui:

- **Canal `C` (clustering, companheiro):** IAAFT tem PODER REAL forte,
  padrão de sucesso equivalente ao já visto em `mse-multiscale-entropy`.
- **Canal `d_B` (box-covering, primário declarado em `METHODOLOGY_NOTE.md`
  Gap (a)):** não é um problema de baixo poder do IAAFT — é um problema
  ANTERIOR e mais básico: a própria grade de escala `l_B` do Gap (a)
  (`l_B_max=floor(diam(G)/4)`, mínimo de 4 valores distintos, i.e.
  `diam(G)>=20`) **não é atingível** para os processos estocásticos
  testados dentro do teto `MAX_N_PER_SEGMENT=5000` do Gap (d). O
  substituto de bootstrap por blocos móveis (pré-autorizado no Gap (e)
  para o padrão de baixo poder do DFA-alpha) foi testado empiricamente e
  **não resolve** esse problema específico, porque ele não é de poder
  estatístico — é de topologia do grafo.

## Achado estrutural (descoberto POR esta validação, não assumido)

Grafos de visibilidade natural de séries temporais estocásticas
(ruído branco, AR(1)/fGn, mapa logístico caótico) são fortemente
"small-world": o diâmetro do grafo cresce apenas como `~log(N)`, porque
os extremos globais da série (máximos/mínimos) atuam como hubs de
visibilidade de longo alcance. Medido diretamente neste laboratório antes
de escrever `validate_synthetic.py`:

| N | processo | diâmetro medido |
|---|---|---|
| 1.000 | ruído branco | 9 |
| 2.000 | ruído branco | 12 |
| 4.000 | ruído branco | 11 |
| 5.000 | ruído branco | 12 |
| 8.000 | ruído branco | 15 |
| 15.000 | ruído branco | 16 |
| 5.000 | passeio aleatório | 14 |
| 5.000 | AR(1) φ=0,95 | 10 |
| 3.000 | mapa logístico r=4 | 16 |
| 5.000 | fGn-like H=0,9 | 17 |
| 5.000 | fGn-like H=0,99 | 19 (estimativa) |

Mesmo empurrando `N` até 15.000 (acima do teto de 5.000 do Gap (d)) e
usando ruído extremamente persistente (H próximo de 1, que já produz
grafos quase densos, caros computacionalmente), o diâmetro raramente
ultrapassa ~17-19 — sempre abaixo do piso de 20 que o Gap (a) exige para
4 escalas. Uma construção puramente determinística sem ruído (rampa
linear/dente-de-serra), que suprime a formação de hubs por quase-
colinearidade, atinge diâmetro 89 em N=2.000 facilmente — mas essa
construção não é representativa de nenhum PRE/POST real esperado nesta
linha (geomagnetismo, hidrologia), só serve como checagem de correção do
próprio código de box-covering (ver `box_covering_code_diagnostic` em
`validation_synthetic.json`: `d_B=1,899`, `N_B(l_B)` calculado com sucesso
em 13 escalas, confirmando que o código CBB + ajuste OLS funciona
corretamente quando a grade é de fato atingível).

**Consequência declarada a priori, agora confirmada:** isso não é uma
falha de implementação (a mesma checagem de correção acima confirma que o
código está certo) — é uma propriedade estrutural do grafo de
visibilidade combinada com a própria convenção de grade do Gap (a)
(`divisor=4`) e o teto de subamostragem do Gap (d) (`MAX_N=5000`).

## Controles sintéticos (N=2.000 cada, `seed=12345`, `N_SURROGATES=200`)

### Controle positivo (`METHODOLOGY_NOTE.md` Gap (b), especificação exata)

PRE = ruído branco Gaussiano iid. POST = mapa logístico caótico (`r=4`),
remapeado por posto (rank-remap) sobre os valores exatos do PRE — marginal
idêntica por construção, espectro confirmado empiricamente quase plano em
ambos (`spectral_exponent_pre=-0,027`, `spectral_exponent_post=+0,022`).

| Canal | PRE real | POST real | Δ real | média nula IAAFT | desvio nulo | p (bicaudal) | desvios-padrão |
|---|---|---|---|---|---|---|---|
| `d_B` | indefinido (2 escalas) | indefinido (1 escala) | indefinido | — | — | — | — |
| `C` | 0,7528 | 0,7933 | +0,04046 | −0,00011 | 0,00279 | **0,0** | **≈14,55σ** |

`C` real cai muito fora da distribuição nula dos 200 substitutos IAAFT —
mesma ordem de grandeza do resultado de MSE nesta linha (~19σ), confirmando
que o coeficiente de clustering do grafo de visibilidade responde a
estrutura NÃO-LINEAR genuína do mapa logístico que o IAAFT (que preserva
apenas espectro linear + marginal) não reproduz.

### Controle negativo (dois sorteios independentes de fGn-like, H=0,7 fixo)

Sonda diretamente o risco de identificabilidade nomeado no Gap (b)
(redundância com a família de Hurst).

| Canal | PRE real | POST real | Δ real | p (bicaudal) | veredito |
|---|---|---|---|---|---|
| `d_B` | indefinido (diam=10) | indefinido (diam=12) | indefinido | — | não computável, não "não significativo" |
| `C` | 0,6088 | 0,5550 | −0,0538 | **0,25** | corretamente não significativo |

## Teste do fallback de bootstrap (pré-autorizado, testado empiricamente)

`METHODOLOGY_NOTE.md` Gap (e) pré-autoriza adicionar bootstrap por blocos
móveis (Kunsch 1989) como teste PRIMÁRIO complementar **se a validação
repetir o padrão de baixo poder já visto em DFA-alpha**. A máquina de
bootstrap (`run_block_bootstrap_test`, `moving_block_bootstrap_resample`)
já foi adicionada a `vg_common.py` como parte da implementação original
(ver módulo, seção "Moving-block bootstrap"), exatamente porque este era um
risco antecipável antes de ver o resultado.

**Mas o padrão encontrado aqui não é o padrão de DFA-alpha.** Em DFA, o
IAAFT calculava `alpha` normalmente nos substitutos, só que a distribuição
nula ficava centrada quase exatamente no valor real (substitutos
preservando o espectro linear reproduziam o mesmo `alpha`) — um problema
de PODER. Aqui, `d_B` frequentemente nem é CALCULADO (`status=
"insufficient_scales"`) — um problema de FORMAÇÃO DA GRADE, anterior a
qualquer teste de significância.

Testado diretamente (25 reamostras de bootstrap por blocos móveis de cada
segmento do controle positivo, comprimento de bloco = `l_B_max` do próprio
segmento — 3 para o PRE, 2 para o POST, conforme a regra do Gap (e)
adendo): **25/25 reamostras do PRE e 25/25 do POST continuaram
`insufficient_scales`**, com diâmetro nas reamostras (10-14) na mesma faixa
do diâmetro original (11-12). O bootstrap por blocos NÃO muda o
comprimento da série nem a propriedade small-world do grafo de
visibilidade daquele tipo de processo — ele reamostra blocos da MESMA série
(preservando sua estrutura local de curto alcance), então herda
exatamente a mesma limitação estrutural. Não faz sentido rodar o protocolo
completo de `N_BOOTSTRAP=1000` dado esse resultado unânime em 25/25 —
desproporcional ao que já está demonstrado (mesmo princípio de escalada
condicional já usado no restante desta linha).

**Conclusão sobre o fallback:** o bootstrap por blocos móveis é uma
correção válida para um problema de PODER estatístico (como em DFA), mas
não é a ferramenta certa para um problema de NÃO-COMPUTABILIDADE
estrutural da grade `l_B`. Nenhuma correção estatística resolve isso —
seria necessário mudar a própria convenção da grade (`divisor`,
`N_SCALES`, teto de subamostragem), o que este passo está **explicitamente
proibido** de fazer (metodologia travada antes do dado real, `METHODOLOGY_
NOTE.md` decidido pelo usuário). Este achado fica registrado para uma
decisão futura do usuário/laboratório, não decidido aqui.

## Veredito de validação — por canal, honesto, sem forçar

- **`C` (clustering):** `IAAFT_HAS_REAL_POWER`. Validado com poder forte
  (~14,55σ no controle positivo, `p=0,25` corretamente não significativo
  no controle negativo). Pronto para aplicação em dado real com o
  protocolo IAAFT como teste PRIMÁRIO, exatamente como especificado no
  Gap (e), sem necessidade do fallback de bootstrap.
- **`d_B` (box-covering):** `NOT_COMPUTABLE_INSUFFICIENT_SCALES`. Não foi
  possível validar poder (positivo OU negativo) porque o canal
  frequentemente não pôde nem ser calculado nos dois controles, sob a
  grade fixada no Gap (a) combinada com o teto do Gap (d). Isso é
  DIFERENTE de "sem sinal" — é "não testável com este protocolo nestes
  comprimentos de segmento". Um agente que rodar `run_vg_analysis` sobre
  dado real deve esperar `status="insufficient_scales"` para `d_B` na
  maioria dos segmentos reais de comprimento comparável, e reportar isso
  honestamente como tal (não como "d_B não mudou" ou qualquer alegação de
  ausência de sinal) — ver `diagnostics.pre_status`/`post_status` no
  retorno de `run_vg_analysis`.

**Nenhum desvio metodológico foi necessário além do que o próprio
`METHODOLOGY_NOTE.md` já pré-autorizava** (a máquina de bootstrap foi
adicionada e testada, conforme Gap (e) previa como possibilidade) — a
convenção de box-covering, a regra PRE/POST, a grade de `l_B`, e o
protocolo de significância permanecem exatamente como fixados, sem
reformulação alguma depois de ver o resultado.

## O que isto significa para o próximo passo (dado real — NÃO parte deste passo)

Quando (em um passo futuro e separado) `run_vg_analysis` for aplicado aos
2 domínios reais (tempestade geomagnética de 17/03/2015, furacão
Harvey/2017), a expectativa honesta, já declarada aqui ANTES de ver
qualquer dado real, é:

- O canal `C` deve produzir um `p_C` interpretável com o protocolo IAAFT
  validado.
- O canal `d_B` provavelmente retornará `status="insufficient_scales"`
  para a maioria ou todos os segmentos PRE/POST, dado que os comprimentos
  de segmento esperados (~milhares de amostras, dentro do teto de 5.000)
  são exatamente a faixa onde esta validação encontrou o problema. Isso
  deve ser reportado como tal — "d_B não pôde ser testado com o protocolo
  especificado nestes comprimentos de segmento" — nunca reinterpretado
  como resultado nulo/negativo de `d_B` em si.
