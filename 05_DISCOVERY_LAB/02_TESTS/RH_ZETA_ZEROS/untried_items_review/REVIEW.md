# RH-REAL — revisão honesta dos itens nunca desenhados como sub-teste (1, 2, 3, 4, 8, 11, 12)

**Status:** `evidence_level: exploratory_only`. NÃO é um pré-registro, NÃO
trava nenhum resultado, NÃO faz nenhuma alegação sobre a Hipótese de
Riemann em si. Autorizado por `DISC-DEC-018` (2026-08-22, onda 4, frente
(a) "RH-REAL-UNTRIED-ITEMS"), continuação de `DISC-RH-REAL-001`
(`CANDIDATE_FORMULATING`, a única linha do portfólio nunca formalmente
fechada). Este documento é o produto dessa frente; a integração em
`TEST_QUEUE.yaml` / `DECISION_LEDGER.yaml` / `DISCOVERY_LAB_STATE.md` /
`README.md` fica para o orquestrador, não para esta sessão.

**Escopo:** dos 12 itens do levantamento de literatura original de
2026-08-12, os itens 7 e 9 já viraram sub-testes completos
(`DISC-RH-GAP-EXTREME-VALUE-SCALING-001`, `REPLICATION_FAILED`-
inconclusivo; `DISC-RH-ZERO-GAP-RUNS-001`, `REPLICATION_PASSED`) e os
itens 5, 6, 10 já foram triados numa segunda passada em 2026-08-21
(`phase0_zeta_eval_triage/TRIAGE_RESULTS.md`; item 10 virou
`DISC-RH-FHK-SHORT-INTERVAL-MAX-001`, `CLOSED_INCONCLUSIVE`). Restam os
itens **1, 2, 3, 4, 8, 11, 12** — nunca desenhados como pergunta própria,
usados apenas na primeira passada de Fase 0 (2026-08-12) como checagem de
que o pipeline reproduz estatísticas GUE/N(T) já conhecidas (validação de
ferramental, não pesquisa).

## Honestidade sobre a fonte: nem todos os 7 itens têm definição persistida

O relatório integral do levantamento de literatura de 2026-08-12 (as 12
definições verbatim, com citações) **nunca foi persistido no
repositório** — só o resumo em `PHASE0_TRIAGE_SUMMARY.md`, o código de
`analysis/phase0_triage.py`/`.json`, e uma frase de prosa em
`TEST_QUEUE.yaml` (`phase0_progress`) sobreviveram. Isso já havia sido
constatado explicitamente pela frente de 2026-08-21
(`TRIAGE_NOTE.md` §0) para os itens 5/6/10, que precisaram ser
*reconstruídos*. A mesma checagem foi refeita aqui, de forma exaustiva
(grep em todo `05_DISCOVERY_LAB/`, `git log` do diretório, busca por
variações textuais "quarto item"/"11th item"/etc.), para os itens 1, 2,
3, 4, 8, 11, 12:

- **Itens 1, 2, 3, 8**: têm definição completa, com código executável e
  resultado numérico, em `analysis/phase0_triage.py` +
  `analysis/phase0_triage_result.json` (rodados sobre `data/zeros1.txt`,
  100.000 zeros reais de Odlyzko). Citações-fonte não estavam no
  repositório com detalhe bibliográfico — verificadas nesta sessão por
  busca direta (ver seção de cada item abaixo).
- **Item 12**: só sobrevive como rótulo de uma frase em
  `PHASE0_TRIAGE_SUMMARY.md` ("variância do número / rigidez GUE",
  marcado `STATUS_UNCERTAIN` pelo agente de pesquisa original, sem
  citação). Reconstruído e verificado nesta sessão (ver item 12 abaixo).
- **Itens 4 e 11**: **nenhum traço no repositório.** Não aparecem em
  `PHASE0_TRIAGE_SUMMARY.md`, não têm função em `phase0_triage.py`, não
  são mencionados em `TEST_QUEUE.yaml`, na sessão de 2026-08-12
  (`09_SESSIONS/2026/2026-08-12_RH_REAL_PHASE0_AND_GAP_RUNS.md`), nem em
  nenhum outro arquivo do laboratório. A numeração "1 a 12" em si só é
  reconstruível para os 10 itens que deixaram algum traço (1, 2, 3, 5, 6,
  7, 8, 9, 10, 12) — para os itens 4 e 11 não existe *nenhum* conteúdo
  para triar. Inventar uma definição agora, sem o relatório original,
  seria fabricar retroativamente o que o "item 4" ou "item 11" diziam —
  exatamente o que a instrução desta frente proíbe. Estes dois itens são
  tratados como **NÃO TRIÁVEIS**, não como "reprovados": é uma lacuna de
  registro do laboratório, não um veredito sobre o conteúdo perdido.

## Tabela de veredito

| Item | Reconstrução / citação verificada nesta sessão | Já checado (Fase 0, 2026-08-12) | Admite pergunta pré-registrável nova, com modelo concorrente nomeado? | Veredito |
|---|---|---|---|---|
| **1. Correlação de pares (Montgomery)** | Montgomery, *"The pair correlation of zeros of the zeta function"*, in *Analytic Number Theory*, Proc. Symp. Pure Math. XXIV, AMS (1973), pp. 181–193. Conjectura R₂(u)=1−(sin πu/πu)² para os zeros, ligada por Dyson às correlações de autovalores GUE. | Sim — `item1_pair_correlation` em `phase0_triage_result.json`: densidade perto de u<0,3 = 0,0111 vs. fundo uniforme 0,1111 (supressão ~10×); densidade em u>1,0 = 0,1165 ≈ fundo uniforme. Repulsão de nível clara, sem correlação de longo alcance na janela testada. | **Não.** É literalmente a estatística GUE de curto alcance sendo confirmada — não há um segundo modelo nomeado que preveja algo *diferente* nesse mesmo regime (curto alcance) para comparar. A pergunta genuinamente aberta sobre correlação de pares é justamente a de *longo* alcance vs. correção de primos — que é o item 12, tratado separadamente abaixo. | **Validação de ferramental, completa. Nenhum sub-teste novo.** |
| **2. Espaçamento GUE (Wigner surmise)** | Mesma conjectura de Montgomery (1973); confirmação numérica massiva desde Odlyzko, *"On the distribution of spacings between zeros of the zeta function"*, Math. Comp. 48(177) (1987), 273–308. | Sim — média do espaçamento normalizado = 0,99999 (esperado 1,0), RMSE histograma vs. Wigner surmise GUE = 0,0306. | **Não.** É *a* estatística canônica de GUE — a mais replicada da literatura (Odlyzko 1987 e dezenas de trabalhos posteriores já a confirmaram em alturas muito maiores que as nossas 100k). Não existe um "modelo concorrente" plausível aqui: qualquer desvio observável seria, por construção, incompatível com décadas de literatura já publicada — testá-lo de novo é replicação, não pergunta nova. | **Validação de ferramental, completa. Nenhum sub-teste novo.** |
| **3. N(T) (fórmula de Riemann–von Mangoldt)** | Von Mangoldt (1905); forma padrão em Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2ª ed. (1986), cap. 9. Teorema **incondicional**, não conjectura. | Sim — resíduo N(T)_real − termo principal ∈ [0,32; 0,59] em 5 pontos de T até 75.000 — consistente com o termo S(T)=O(log T) esperado. | **Não.** É teorema provado, não falsificável. O resíduo é exatamente S(t), cujo comportamento estatístico fino (momentos, TCL) já foi coberto pelos itens 5 e 6 da segunda triagem (2026-08-21, despriorizados por serem também teoremas / observável não-informativo em altura finita). Reabrir aqui seria duplicar aquela análise. | **Validação de ferramental, completa. Nenhum sub-teste novo.** |
| **4. (sem definição persistida)** | — | — | Não avaliável — não há o que triar. | **NÃO TRIÁVEL.** Lacuna de registro do laboratório (ver seção acima), não um veredito sobre conteúdo. |
| **8. Gap máximo (Bui & Milinovich)** | H. M. Bui e M. B. Milinovich, *"Gaps between zeros of the Riemann zeta-function"*, Q. J. Math. 69(2) (2018), 403–423 (arXiv:1410.3635) — provam que existem infinitos gaps consecutivos > 3,18× o espaçamento médio local. | Sim — máximo observado nos 100k zeros: 2,8052, não excede 3,18 (esperado — o teorema é sobre existência em alturas suficientemente grandes, não detectável nesta faixa). | **Não.** É um teorema de existência assintótica (∃ infinitos gaps grandes em alguma altura não especificada) — estruturalmente do mesmo tipo do item 7 (liminf de Inoue) já descartado na triagem anterior por não admitir pergunta falsificável com dado finito. Não há um segundo modelo nomeado prevendo um limiar *diferente* para comparar; o único "teste" possível é "o máximo já excedeu 3,18?", que não é falsificável (um "não" a qualquer altura finita nunca refuta o teorema). | **Validação de ferramental, completa. Nenhum sub-teste novo.** |
| **11. (sem definição persistida)** | — | — | Não avaliável — não há o que triar. | **NÃO TRIÁVEL.** Lacuna de registro do laboratório (ver seção acima), não um veredito sobre conteúdo. |
| **12. Variância do número / rigidez GUE** | Berry, M. V., *"Semiclassical formula for the number variance of the Riemann zeros"*, Nonlinearity 1 (1988), 399–407 (conjectura, dois regimes). Prova condicional recente: Lugar, Milinovich & Quesada-Herrera, *"On the number variance of zeta zeros and a conjecture of Berry"*, arXiv:2211.14918 (2022) — prova a Conjectura de Berry no regime não-universal assumindo RH **e** uma extensão de Chan (2004, *"Pair correlation of the zeros of the Riemann zeta function in longer ranges"*, Acta Arith. 115, 181–204) da conjectura de correlação de pares de Montgomery. | Não coberto por nenhuma triagem anterior — nem a de 2026-08-12 (que só cobriu correlação de curto alcance, item 1) nem a de 2026-08-21 (que cobriu momentos/TCL/máximos, não variância do número). | **Sim.** Ver piloto de viabilidade completo abaixo. | **ÚNICO CANDIDATO GENUÍNO desta leva.** Recomendado para pré-registro real (não travado aqui). |

## Por que os itens 1, 2, 3, 8 não rendem sub-teste (resumo em uma frase cada)

- **1 e 2** já **são** a estatística GUE de curto alcance — testá-los de
  novo é replicar Odlyzko (1987) e sucessores, não formular pergunta
  nova.
- **3** é teorema incondicional; seu resíduo (S(t)) já foi coberto pelos
  itens 5/6 da triagem de 2026-08-21.
- **8** (como o já descartado item 7) é um resultado de *existência*
  assintótica — não admite critério de falsificação com dado de altura
  finita, e não há um segundo modelo nomeado prevendo algo diferente
  para comparar.

Isto é um veredito honesto e completo, não uma falha de busca: o próprio
propósito original destes 4 itens (junto com o 1, 2, 3 já discutidos) na
sessão de 2026-08-12 era validar o pipeline contra estatística já
conhecida — cumpriram esse papel integralmente.

---

## Item 12 — piloto de viabilidade (não pré-registro)

### A estatística exata

Número de zeros renormalizados (𝒩(γ)=γ/2π·(log(γ/2π)−1)+7/8, espaçamento
médio exatamente 1) numa janela deslizante de comprimento `L`: contagem
`n(L;x)`, variância `V(L) := Var[n(L;x) − L]` sobre muitas posições `x`.
Berry (1988), Conjectura 1.4.1 (citada via arXiv:2211.14918 eq. 1.19 e
Conjecture 1.4.1), dá uma fórmula fechada única que se especializa em
dois regimes:

- **Regime universal** (`L = o(log T)`): `V(L) ~ (1/π²)[log(2πL) −
  Ci(2πL) − 2πL·Si(2πL) + π²L − cos(2πL) + 1 + γ₀]` — **coincide
  exatamente com a variância de autovalores GUE**.
- **Regime não-universal** (`L ≫ log T`): `V(L) ~ (1/π²)[Σ_{n≤T}
  (Λ²(n)/(n·log²n))·(1 − cos(2πL·log n/log T)) + 1]` — soma sobre
  potências de primos `n=pᵏ`; **não é mais GUE**, incorpora primos.

### Modelos concorrentes nomeados

- **Modelo A** ("GUE puro/estendido"): a fórmula do regime universal
  avaliada em qualquer `L`, inclusive fora de `L=o(log T)` — é a hipótese
  ingênua "a rigidez GUE de curto alcance continua valendo em qualquer
  escala".
- **Modelo B** (Berry / correção aritmética): a fórmula do regime
  não-universal — hoje um **teorema condicional** (RH + Conjectura de
  Chan 2004) para `L = o(log^{4/3}T)`, não mais só conjectura.

Esta é exatamente a estrutura exigida pela tarefa: previsão numérica
precisa (não "reproduz GUE", já que os dois modelos divergem fora do
regime universal), modelo concorrente nomeado e distinguível, e dado real
suficiente — os três datasets Odlyzko já em `data/` (`zeros1.txt`,
100.000 zeros até T≈75.000; `zeros3.txt`, 10.000 zeros perto do zero
#10¹², T≈2,68×10¹¹; `zeros4.txt`, 10.000 zeros perto do zero #10²¹,
T≈1,44×10²⁰) cobrem justamente o tipo de janela estreita-em-altura-alta
que este teste precisa (log T ≈ 11,2 / 26,3 / 46,4 respectivamente —
dando bastante alcance de `L` acima de log T em cada um).

### O que o piloto computou

Script `item12_number_variance_pilot.py` (log completo em
`item12_number_variance_pilot.log`, resultado em
`item12_number_variance_pilot_result.json`), rodado uma única vez em
primeiro plano, ~22s de parede:

1. `V(L)` empírico via janela deslizante (passo `L/4`) para os 3
   datasets, grade de `L` de 1 a 3000 (zeros1) / 1500 (zeros3, zeros4).
2. Modelo A fechado (via `scipy.special.sici`), exato, barato.
3. Modelo B: **exato** para zeros1 (T≈74.921, todas as 7.486 potências de
   primos ≤ T enumeradas via `sympy.primerange` — viável porque T é
   pequeno); **truncado** (primos ≤ 10⁷) para zeros3/zeros4, onde
   enumerar todos os primos até T≈10¹¹/10²⁰ é inviável — a fração
   estimada da soma capturada (via Mertens) é ≈86% (zeros3) e ≈74%
   (zeros4), reportada explicitamente como sub-estimativa, não como
   valor real do modelo.

### Resultado (achado qualitativo, não decisivo)

Para `L` pequeno (dentro do regime universal nominal, `L ≲ log T`), o
empírico acompanha o Modelo A razoavelmente bem — consistente com o que
os itens 1/2 já confirmaram para correlações de curto alcance. Mas para
`L` bem além de `log T` (que é exatamente onde a distinção entre os dois
modelos importa), o padrão nos três datasets independentes é o mesmo:

| Dataset | log T | V_emp em L pequeno (L=1) | V_emp em L grande | Modelo A em L grande | Modelo B em L grande |
|---|---|---|---|---|---|
| zeros1 (T≈7,5×10⁴) | 11,22 | 0,321 (L=1) | 0,41–0,51 (L=1000–3000) | 1,05–1,16 (cresce sem limite) | 0,40–0,43 (EXATO) |
| zeros3 (T≈2,68×10¹¹) | 26,31 | 0,341 (L=1) | 0,30–0,57 (L=500–1500) | 0,98–1,09 | 0,38–0,49 (truncado, ≥) |
| zeros4 (T≈1,44×10²⁰) | 46,42 | 0,345 (L=1) | 0,39–0,58 (L=500–1500) | 0,98–1,09 | 0,39–0,46 (truncado, ≥) |

Em `L` grande, o Modelo A (GUE estendido ingenuamente) cresce sem limite
(`~log L`) e se afasta cada vez mais do dado real; o dado real fica
**achatado/limitado**, muito mais perto do Modelo B — em zeros1, onde o
Modelo B pôde ser calculado exatamente (não truncado), a concordância
qualitativa é boa (diferenças de ordem 0,05–0,15, mesma faixa da própria
variação ponto-a-ponto do dado). O mesmo padrão qualitativo aparece nos
três regimes de altura, ~15 ordens de magnitude à parte — reforço
razoável de que não é acidente do dataset.

**Verificação de sanidade do estimador**: o cálculo por janelas
deslizantes sobrepostas foi conferido de forma independente com um
estimador de janelas *não sobrepostas* (mais simples, menos amostras,
sem viés de correlação de sobreposição) para zeros1 — mesmo padrão de
achatamento confirmado (V≈0,45–0,54 para L=10 a 3000, sem crescimento
sistemático), descartando que o achado seja um artefato do estimador
com sobreposição.

### Limitações honestas deste piloto (não resolvidas — ficam para o pré-registro real)

1. **Não houve nota pré-computação travada antes de rodar o script**
   (diferente da disciplina seguida por `TRIAGE_NOTE.md` da frente de
   2026-08-21). O script rodou uma única vez, sem iteração/ajuste após
   ver o resultado — não há p-hacking de parâmetros —, mas a ausência de
   um critério de decisão travado a priori é uma lacuna de processo desta
   sessão, registrada aqui sem maquiagem. Um pré-registro real **precisa**
   fixar a grade de `L`, o estimador exato e o limiar de decisão antes de
   qualquer cômputo.
2. **Estimador de `V(L)` simplificado**: janela deslizante ad hoc, não o
   estimador suavizado exato `V(L;x)` (com parâmetro de suavização `Δx`)
   definido no Teorema 1.3.1 do paper-fonte. Precisa ser substituído pelo
   estimador correto e justificado.
3. **Aproximação δ≈L**: usada por construção exata (ambos definidos como
   "contagem esperada na janela"), mas a equivalência com a normalização
   exata `2πδ/log T` do enunciado de Berry precisa de justificativa
   formal explícita no pré-registro, não só argumentada em prosa aqui.
4. **Modelo B truncado para zeros3/zeros4**: os números reportados para
   estes dois datasets são cotas inferiores (sub-estimativas), não o
   valor real do modelo — um pré-registro real precisa de soma sobre
   primos até T exato (inviável por enumeração direta em T~10¹¹/10²⁰) ou
   de uma aproximação analítica com erro rigorosamente limitado (soma
   parcial de Mertens), não uma truncagem ad hoc.
5. **Poucas janelas independentes em L grande** para zeros3/zeros4 (23
   janelas em L=1500, mesmo com sobreposição) — poder estatístico não
   quantificado; provavelmente insuficiente sem mais zeros nessas
   alturas (zeros5.txt, regime #10²², citado em `PROVENANCE.md` como
   "ainda não baixado", é candidato natural a dado adicional).
6. **Nenhum framework de significância/decisão** (sem nulo por
   permutação, sem limiar travado, sem correção por comparações
   múltiplas em `L`) — isto é um esboço de viabilidade, não um teste de
   hipótese.
7. **Nenhuma alegação sobre RH**: o Modelo B é, ele mesmo, um teorema
   condicional a RH (e a Conjectura de Chan). Os zeros usados aqui são
   computados sob a suposição de que estão na linha crítica (é assim que
   as tabelas de Odlyzko são construídas) — o piloto não testa RH, apenas
   compara dois modelos de estatística de zeros *dado* que eles estão na
   linha crítica, exatamente como todos os testes anteriores desta linha.

Apesar dessas limitações, o padrão é forte o bastante (mesmo sinal
qualitativo em 3 regimes de altura independentes, incluindo uma
comparação EXATA — não truncada — contra o Modelo B em zeros1) para
justificar investimento num pré-registro de verdade, com poder
provavelmente melhor do que o que `DISC-RH-FHK-SHORT-INTERVAL-MAX-001`
(item 10) conseguiu.

---

## Recomendação

**Não** "nenhum item novo rende sub-teste genuíno" — esse NÃO é o
resultado desta revisão. Dos 7 itens revisados, 4 (1, 2, 3, 8) são
veredictos honestos de "validação de ferramental completa, sem pergunta
nova", 2 (4, 11) são "não triável, lacuna de registro do laboratório", e
**1 (item 12, variância do número) admite uma pergunta pré-registrável
genuína**, com modelo concorrente nomeado, dado real já disponível, e um
piloto de viabilidade que mostra um sinal qualitativo forte e
reproduzível em três regimes de altura independentes.

**Candidato único recomendado para o próximo pré-registro real:** item
12 (variância do número dos zeros de zeta: GUE estendida ingenuamente
vs. correção aritmética de Berry, provada condicionalmente por
Lugar–Milinovich–Quesada-Herrera 2022). Esta é só uma recomendação — como
sempre nesta linha, nenhum pré-registro foi desenhado ou travado nesta
sessão; a decisão de seguir (ou não) é de governança futura, fora desta
frente. Se seguida, um pré-registro real precisaria minimamente:
critério de decisão e grade de `L`/alturas travados a priori; estimador
exato `V(L;x)` (com `Δx` declarado) substituindo o ad hoc usado aqui;
Modelo B calculado sem truncagem (ou com erro de truncagem rigorosamente
limitado) em pelo menos um regime de altura alta; e, seguindo o padrão já
estabelecido pela linha (`DISC-RH-ZERO-GAP-RUNS-001`), verificação
adversarial independente antes de qualquer alegação de achado.

## Arquivos desta frente

- `REVIEW.md` (este arquivo).
- `item12_number_variance_pilot.py` — script do piloto de viabilidade.
- `item12_number_variance_pilot_result.json` — resultado numérico
  completo (todos os datasets, todos os `L`, ambos os modelos).
- `item12_number_variance_pilot.log` — saída completa da execução.

Nenhum arquivo pré-existente de `RH_ZETA_ZEROS/` foi modificado. Nenhuma
computação em segundo plano foi deixada rodando (script rodou em
primeiro plano, ~22s). Nenhuma alegação sobre a Hipótese de Riemann é
feita ou implicada por este documento.
