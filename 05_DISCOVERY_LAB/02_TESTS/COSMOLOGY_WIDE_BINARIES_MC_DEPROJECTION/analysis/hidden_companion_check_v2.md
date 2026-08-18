# Checagem de multiplicidade oculta REFEITA com o sinal CORRIGIDO — `DISC-COSMOLOGY-MOND-SPARC-004`

**Contexto:** a checagem adversarial original (`hidden_companion_check.json`/`.md`)
foi calculada sobre `result_primary.json` (v1), **afetado** pelo bug de
assimetria de ruído astrométrico documentado em `PREREGISTRATION.md` Seção
5b. O sinal bruto ali era grande (`δ_obs-newt` = `+0,227` a `+0,047`). Após
a correção do bug e a reexecução real (`result_primary_v2.json`), o sinal
residual real ficou **muito menor** (`δ_obs-newt` = `+0,1486; +0,1482;
+0,1150; +0,0949; +0,0430`, IC95% do `a0` ajustado = `[1,232×10⁻¹⁰;
2,181×10⁻¹⁰]`, veredito bruto `BOTH_FALSIFIED`). O gatilho de multiplicidade
oculta continua ativo (`g/g_N` bruto do bin 0 = `1,0099>1`). Esta checagem
refaz os 3 itens da checagem original com o sinal **corrigido** como alvo,
usando a pipeline **corrigida** (ruído astrométrico simétrico nos dois
ramos, em toda chamada de `don.run_delta_obs_newt` abaixo).

**Script:** `analysis/hidden_companion_check_v2.py`. **Dados brutos
completos:** `analysis/hidden_companion_check_v2.json`. **Arquivos
travados usados sem edição** (`delta_obs_newt.py`, `deprojection_common.py`)
— confirmado via `git diff` ao final da sessão que permanecem intocados.

## Resumo executivo

| item | resultado |
|---|---|
| 1. estimativa analítica (só inflação de massa) | magnitude ~`+0,034` a `+0,063` dex (f_multi 0,25–0,47) — agora cobre de **23% a 146%** do sinal real por bin (era ~12–25% no sinal com bug); no bin de menor g_N (bin 4, real=`+0,043`) a inflação de massa **sozinha, sem wobble**, já cobre de **79% a 146%** — pode sozinha explicar ou até superexplicar esse bin |
| 2. teste direto RUWE alto vs. baixo (pipeline corrigida) | diferença **ainda grande e estatisticamente significativa em todos os 5 bins** (RUWE alto sempre maior, IC95% não se sobrepõe, diferença `+0,155` a `+0,377`) — proporcionalmente **maior** que o sinal real total em quase todos os bins agora |
| 3. simulação MC própria de injeção (massa+wobble), varredura f_multi=0,25–0,47 | **mesmo no limite inferior da faixa observacional (f_multi=0,25)**, o sinal sintético (zero MOND) **já iguala ou excede** o sinal real corrigido em todos os 5 bins (razão sintético/real de `1,25×` a `3,46×`); nenhum f_multi testado reproduz a FORMA declinante completa dentro do IC95% simultaneamente nos 5 bins, mas isso é porque o modelo simplificado de wobble **superestima** o bin de maior g_N, não porque falte magnitude |

**Veredito da Parte 2 (v2):** com o sinal corrigido (bem menor), a
multiplicidade oculta não corrigida **é plausivelmente suficiente, sozinha,
para explicar o sinal residual observado inteiro** — ao contrário da
checagem original (feita sobre o sinal com bug, ~5× maior), onde a
multiplicidade contribuía mas claramente não bastava. Isso **enfraquece
significativamente** a confiabilidade do veredito bruto `BOTH_FALSIFIED`
como evidência de física nova: um artefato mundano e já conhecido
(companheiras não resolvidas, RUWE, Chae 2023 Seção 3.2), em magnitude
plausível pela literatura, já é suficiente para produzir um sinal do
tamanho observado sem qualquer boost MOND.

---

## Item 1 — estimativa analítica de magnitude (Chae Eqs. 11–13, reimplementada)

Mesmo mecanismo da checagem original (inflação de massa fotométrica pura,
sem wobble): uma companheira oculta não resolvida faz o pipeline de massa
(`M(L)=L^(1/3,5)`, côncava) subestimar a massa total verdadeira do
componente afetado por um fator `B(κ)=κ^(1/3,5)+(1-κ)^(1/3,5)≥1`. Reimplementado
aqui de forma **ligada aos `M1_Msun`/`M2_Msun` REAIS de cada um dos 30.203
sistemas** (não um número de população abstrato) — atribuição de Chae
(40% só componente brilhante, 30% só o fraco, 30% ambos), `κ` amostrado de
uma lei de potência `γ_M=-0,7` (Tokovinin 2008) em `ΔM_G∈[0,01; 5,0]` mag.

| f_multi | deslocamento populacional médio esperado (dex) | fração do sinal real — bin0 | bin1 | bin2 | bin3 | bin4 |
|---|---|---|---|---|---|---|
| 0,25 | +0,034 | 22,8% | 22,9% | 29,5% | 35,7% | **78,9%** |
| 0,30 | +0,040 | 27,2% | 27,2% | 35,1% | 42,5% | **93,8%** |
| 0,35 | +0,047 | 31,6% | 31,7% | 40,9% | 49,5% | **109,3%** |
| 0,40 | +0,054 | 36,4% | 36,5% | 47,1% | 57,0% | **125,8%** |
| 0,47 | +0,063 | 42,1% | 42,2% | 54,4% | 66,0% | **145,6%** |

(sinal real por bin: `+0,1486; +0,1482; +0,1150; +0,0949; +0,0430`)

**Validação cruzada:** o deslocamento médio calculado aqui (analítico, sem
órbita) bate bem com o resultado "mass-only" (sem wobble) da simulação MC
completa do Item 3 (`f_multi=0,40`: `+0,051; +0,029; +0,052; +0,040;
+0,052` por bin — comparável a `+0,054` esperado aqui, e note que a
simulação completa já produz uma leve variação por bin mesmo num mecanismo
"constante" por causa da interação não-linear entre o deslocamento e a
mediana da distribuição completa por bin, não capturada pela estimativa
puramente populacional).

**Leitura:** diferente da checagem original (onde a inflação de massa
sozinha cobria só ~25% do bin de maior sinal, mesmo no limite superior de
`f_multi`), agora — com o sinal real ~5× menor — a inflação de massa
**sozinha, sem qualquer mecanismo de wobble**, já cobre de **79% a 146%**
do sinal real no bin de menor g_N (bin 4), e uma fração substancial
(23–66%) nos demais bins. O mecanismo de massa continua sendo
aproximadamente CONSTANTE através dos bins (não depende de g_N), então
proporcionalmente ele agora "sobra" mais nos bins de sinal pequeno
(bin 4) do que nos de sinal grande (bin 0).

## Item 2 — teste direto: RUWE alto vs. RUWE baixo, pipeline CORRIGIDA

`RUWE_max=max(RUWE1,RUWE2)` por sistema, limiar `>1,2` (convenção comum de
excesso astrométrico, Lindegren et al. 2021). **31,06%** da amostra de
descoberta (9.380/30.203) tem `RUWE_max>1,2`. Pipeline travada
(`don.run_delta_obs_newt`, `n_mc=200`, `n_bootstrap=500`, ruído
astrométrico simétrico no ramo mock — Seção 5b) rodada **separadamente**
nos dois subconjuntos.

| bin | δ (RUWE alto, n=9.380) | δ (RUWE baixo, n=20.823) | diferença | IC95% se sobrepõe? |
|---|---|---|---|---|
| 0 | +0,4598 [0,402; 0,518] | +0,0828 [0,053; 0,114] | **+0,3770** | não |
| 1 | +0,4330 [0,376; 0,488] | +0,0620 [0,035; 0,094] | **+0,3710** | não |
| 2 | +0,3495 [0,296; 0,400] | +0,0321 [0,004; 0,060] | **+0,3174** | não |
| 3 | +0,2893 [0,244; 0,334] | +0,0240 [−0,007; 0,053] | **+0,2653** | não |
| 4 | +0,1312 [0,098; 0,164] | −0,0233 [−0,056; 0,009] | **+0,1545** | não |

Em **todos os 5 bins**, RUWE alto mostra excesso muito maior (0,15–0,38 dex
a mais) que RUWE baixo, com IC95% claramente não se sobrepondo — **mesma
conclusão qualitativa da checagem original**, mas agora com uma leitura
proporcional muito mais forte: a diferença absoluta (alto−baixo) é
praticamente **igual ou maior** em magnitude à do sinal com bug (que era
`+0,339` a `+0,157`), mas o sinal real TOTAL encolheu ~5×. Ou seja, o efeito
associado a RUWE não encolheu com a correção do bug — ele é, proporcionalmente,
uma fração **muito maior** do sinal real corrigido do que era antes
(diferença bin0 `+0,377` vs. sinal real total do bin0 `+0,1486` — a
diferença RUWE sozinha já é **2,5× maior** que o sinal real inteiro).

O subconjunto RUWE baixo, isolado, já mostra δ compatível com zero em
**3 dos 5 bins** (bin2 IC `[0,004;0,060]` toca zero na borda, bin3 IC
`[−0,007;0,053]` contém zero, bin4 IC `[−0,056;0,009]` contém zero
folgadamente) — só os bins 0–1 (menor g_N) retêm um resíduo pequeno mas
não-nulo (`+0,083`, `+0,062`) mesmo no subconjunto mais "limpo" de RUWE.

**Confundidor já documentado (mantido da checagem original, ainda válido):**
a fração de RUWE alto aumenta com o bin (23,5% no bin 0 até 49,1% no bin 4,
mediana de RUWE_max de 1,079 a 1,193) — direção OPOSTA à necessária para
explicar o declínio de δ com g_N puramente por composição populacional.

## Item 3 — simulação Monte Carlo própria de injeção (mass inflation + photocenter wobble)

Reimplementação própria (não reaproveita `don.generate_synthetic_vp_newtonian`
— chama só as funções públicas travadas `dc.sample_eccentricity`/
`dc.sample_orbital_geometry`, exigido pela mesma metodologia de
desprojeção). Para um conjunto **puramente Newtoniano** (zero física MOND)
com a MESMA distribuição real de massa (`M1_Msun`/`M2_Msun`), separação,
excentricidade (catálogo de Hwang) e erro de PM (Gaia) dos 30.203 sistemas
de descoberta reais, injeta:

1. **Inflação de massa** (Item 1) — atribuição 40%/30%/30%, `κ` amostrado
   independentemente por componente afetado.
2. **Wobble de fotocentro** — fórmula padrão de astrometria binária
   (`β = fração_de_massa − fração_de_luz` da sub-componente minoritária),
   semi-eixo interno `a_in` log-uniforme em `[0,01; d_pc]` UA (Belokurov
   et al. 2020, citado por Chae — limite superior = 1 arcsec não resolvido),
   órbita interna circular aproximada (fase uniforme, simplificação
   declarada), velocidade de wobble `=|β|·v_orb_inner`, somada
   VETORIALMENTE (ângulo relativo aleatório) ao `v_p` externo.
3. `M_tot` passado à pipeline (ambos os ramos) é sempre a massa catalogada
   **não-corrigida** (`M1_Msun+M2_Msun` reais) — exatamente como o pipeline
   real opera.
4. O `v_p` sintético "real" recebe o MESMO orçamento de ruído astrométrico
   Gaussiano simétrico (por sistema, erros de PM reais do Gaia) que o ramo
   mock interno de `don.run_delta_obs_newt` também recebe — Seção 5b.

| cenário | δ bin0 | δ bin1 | δ bin2 | δ bin3 | δ bin4 |
|---|---|---|---|---|---|
| **real observado (corrigido)** | +0,1486 | +0,1482 | +0,1150 | +0,0949 | +0,0430 |
| f_multi=0,25, com wobble | +0,2034 | +0,1849 | +0,1571 | +0,1344 | +0,1487 |
| f_multi=0,30, com wobble | +0,2256 | +0,1939 | +0,2027 | +0,1879 | +0,1673 |
| f_multi=0,35, com wobble | +0,3144 | +0,2521 | +0,2576 | +0,2154 | +0,2216 |
| f_multi=0,40, com wobble | +0,3629 | +0,2998 | +0,2885 | +0,2694 | +0,2443 |
| f_multi=0,47, com wobble | +0,4955 | +0,4379 | +0,4101 | +0,3283 | +0,2903 |
| f_multi=0,40, SÓ massa (sem wobble) | +0,0509 | +0,0294 | +0,0520 | +0,0400 | +0,0515 |

Razão sintético/real por bin (f_multi=0,25, o limite INFERIOR da faixa
observacional): `1,37×; 1,25×; 1,37×; 1,42×; 3,46×`. **Mesmo no extremo
mais conservador da faixa plausível, a magnitude sintética já é maior que
o sinal real inteiro, em todos os 5 bins.**

### Pergunta central: existe f_multi∈[0,25;0,47] cujo IC95% sintético cubra o IC95% real nos 5 bins simultaneamente?

| f_multi | overlap IC95% por bin (0,1,2,3,4) | todos os 5 bins? |
|---|---|---|
| 0,25 | [não, **sim**, **sim**, **sim**, não] | não |
| 0,30 | [não, **sim**, não, não, não] | não |
| 0,35 | [não, não, não, não, não] | não |
| 0,40 | [não, não, não, não, não] | não |
| 0,47 | [não, não, não, não, não] | não |

**Resposta formal, literal:** não — nenhum `f_multi` isolado da varredura
reproduz o IC95% real nos 5 bins simultaneamente. Mas a razão é
informativa: em `f_multi=0,25` (o extremo INFERIOR da faixa), o IC95%
sintético já **se sobrepõe ao real em 3 dos 5 bins** (1, 2, 3), e nos 2
bins onde não se sobrepõe (0 e 4), o sintético está **acima** do real, não
abaixo — ou seja, o modelo de injeção **superestima**, não subestima, o
sinal. O padrão de falha é de FORMA (o mecanismo de wobble, nesta
implementação simplificada — fase interna uniforme, `a_in` log-uniforme
sem ponderação temporal — não decai o suficiente em alta g_N, mesmo
problema qualitativo já identificado na checagem original), não de
MAGNITUDE INSUFICIENTE. Um `f_multi` moderadamente ABAIXO de 0,25 (fora da
faixa observacional testada aqui, mas não necessariamente irreal — a
faixa 0,25–0,47 é uma faixa observacional agregada de vários levantamentos,
não um limite físico rígido) provavelmente reproduziria a magnitude nos
bins 0–3 com folga, mantendo o mesmo problema de forma no bin 4.

## Veredito consolidado da Parte 2 (v2)

Com o sinal corrigido (`~5×` menor que o sinal com bug usado na checagem
original), a leitura muda substancialmente:

1. **Item 2 (RUWE) continua sendo evidência direta, forte e não-ambígua**
   de que multiplicidade oculta contribui — e agora, proporcionalmente ao
   sinal real menor, essa contribuição é ainda mais dominante (a diferença
   RUWE alto−baixo sozinha excede o sinal real total em vários bins).
2. **Item 1 (massa sozinha)**, que na checagem original cobria apenas
   ~25% do sinal mesmo no limite superior de `f_multi`, agora cobre de
   **79% a 146%** do sinal no bin de menor g_N — plausivelmente suficiente
   sozinho ali, sem precisar de wobble ou qualquer outro mecanismo.
3. **Item 3 (simulação própria completa)** mostra que mesmo o limite
   INFERIOR da faixa observacional de `f_multi` (0,25) já produz um sinal
   sintético (zero MOND) **maior** que o sinal real inteiro em todos os 5
   bins — a "sobra" de magnitude é tão grande que o desalinhamento de forma
   (bin de maior g_N) é a única coisa impedindo um "match" formal completo,
   não falta de amplitude.

**Conclusão:** ao contrário da checagem original (onde a multiplicidade
contribuía mas claramente não bastava para explicar o sinal com bug), com
o sinal CORRIGIDO a evidência aponta na direção oposta: **multiplicidade
oculta não corrigida, em magnitude inteiramente plausível pela literatura
(`f_multi=0,25–0,47`, Tokovinin 2014b, Riddle et al. 2015, Moe & Stefano
2017, Raghavan et al. 2010), é suficiente — e provavelmente MAIS que
suficiente — para produzir um sinal do tamanho e ordem de grandeza do
resíduo real observado, sem qualquer física MOND.** O desalinhamento de
FORMA entre a simulação simplificada e o padrão real declinante é uma
limitação conhecida desta implementação aproximada de wobble (mesma
limitação já identificada na checagem original), não evidência de que a
magnitude seja insuficiente — é o oposto: a magnitude sobra.

**Implicação para o veredito `BOTH_FALSIFIED` de `result_primary_v2.json`:**
esse veredito bruto foi calculado sobre um `δ_obs-newt` que, por esta
checagem, é plausivelmente explicável em grande parte ou inteiramente por
um artefato mundano e conhecido (companheiras não resolvidas, já nomeado e
declarado como simplificação NÃO implementada na Seção 4 do
pré-registro). Isso **enfraquece — não fortalece — a confiabilidade do
veredito `BOTH_FALSIFIED` como evidência de física nova**: se
multiplicidade oculta explica todo (ou quase todo) o sinal residual, o
`a0` ajustado de `1,657×10⁻¹⁰` m/s² (IC95% `[1,232×10⁻¹⁰; 2,181×10⁻¹⁰]`) e
a exclusão de `a0_A`/`a0_B` do IC não refletem necessariamente física MOND
genuína — podem refletir, em vez disso, um viés sistemático conhecido e
não corrigido. Diferente da checagem original (que recomendava manter o
veredito, já que multiplicidade só explicava parte do sinal), esta
checagem recomenda **não aceitar `BOTH_FALSIFIED` como conclusão robusta
por este canal** sem antes implementar a correção completa de `f_multi`
de Chae (Seção 4, "Simplificação declarada" — auto-calibração completa,
não a aproximação desta checagem adversarial) e repetir a análise
primária com essa correção aplicada.

## Limitações desta checagem

- O modelo de wobble usa fase orbital interna uniforme (não ponderada pelo
  tempo) e `a_in` log-uniforme em `[0,01;d_pc]` UA sem levar em conta a
  distância específica do componente afetado — simplificações declaradas
  (mesmas limitações já identificadas na checagem original), que
  provavelmente explicam por que o sintético não decai o suficiente em
  alta g_N (bin 4).
- A fórmula de `β` (fração de deslocamento fotocentro-baricentro) usada
  aqui é a formulação padrão de astrometria binária
  (`β=M_a/(M_a+M_b)−L_a/(L_a+L_b)`), não uma reprodução literal das
  Eqs. 19–20 de Chae (2023) — não foi feita nova verificação linha-a-linha
  do texto do artigo nesta sessão (reaproveitado o mesmo nível de
  aproximação já usado na checagem original).
- RUWE é um proxy imperfeito e incompleto de multiplicidade oculta (não
  detecta todas as companheiras não resolvidas) — mesma ressalva já
  documentada na checagem original.
- `n_bootstrap=500` (Itens 2 e 3) em vez de `1000` (usado na análise
  primária) — decisão de compromisso para viabilizar 8 reexecuções
  completas da pipeline nesta checagem em tempo razoável; ainda >> 100
  exigido por Chae (2023) para a mediana de um bin ser bem determinada.
- Não implementei a auto-calibração completa de `f_multi` de Chae (que
  ajusta `f_multi` contra a convergência ao Newtoniano em alta aceleração)
  — usei valores fixos varridos na faixa observacional da literatura, não
  uma re-derivação própria contra os dados.
- Um bug de implementação real foi encontrado e corrigido durante esta
  sessão (Item 1 usava a MEDIANA populacional do deslocamento de massa em
  vez da MÉDIA — a mediana é matematicamente 0 sempre que `f_multi<0,5`,
  por construção, o que é correto mas não é o proxy útil para o
  deslocamento esperado na estatística de mediana da amostra INTEIRA).
  Corrigido em `hidden_companion_check_v2.py` antes da entrega deste
  relatório; documentado no código-fonte com nota completa.
