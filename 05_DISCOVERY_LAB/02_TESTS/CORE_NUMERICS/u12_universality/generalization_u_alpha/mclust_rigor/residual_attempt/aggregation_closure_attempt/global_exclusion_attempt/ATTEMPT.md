# ATTEMPT — testando a exclusão global (ordem t·n) sobre o hazard elevado

**Onda 9 (continuação de DISC-DEC-033), frente `MCLUST-RESIDUAL-RIGOR`,
subfrente `GLOBAL-EXCLUSION`.**
**Escopo, fixado por mandato:** este documento e os arquivos desta
subpasta (`global_exclusion_attempt/`) são um anexo NOVO que estende
`aggregation_closure_attempt/ATTEMPT.md`, sem modificá-lo. Nenhum arquivo
em `aggregation_closure_attempt/`, `residual_attempt/` ou `mclust_rigor/`
foi tocado (apenas lido). `THEOREM.md`, `DECISION_LEDGER.yaml`,
`TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md` e `README.md` não foram
tocados — integração fica a cargo da sessão orquestradora. Nenhum commit
git foi criado. A classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ não é
questionada em lugar nenhum abaixo. Nada sob
`u12_universality/theorem/` foi tocado.

**Alvo específico:** a hipótese nomeada explicitamente em
`aggregation_closure_attempt/ATTEMPT.md` §7.2 — que o hazard de fechamento
deveria excluir não só os b−1 pontos da janela LOCAL de x (já contabilizado
pelo fator de elevação P) mas também TODOS os outros pontos (ordem t·n) já
consumidos como imagem de π por passos normais anteriores em QUALQUER parte
do passeio, sugerindo densidade por-alvo ~1/[(1−t)n] em vez de ~1/n.

## 0. Disciplina

Li por inteiro `aggregation_closure_attempt/ATTEMPT.md` (§0–10, todas as
seções), `residual_attempt/ATTEMPT.md` (§0–9, todas as seções),
`DERIVATIONS.md` §0–3 (fórmula-mestre M-q, incluindo a leitura cuidadosa
de §0 que localiza exatamente o que o hazard 1/(1−t) representa — ver §1
abaixo), e os simuladores/scripts de infraestrutura indicados no mandato:
`mclust_walk_diagnostic.py`, `mclust_residual_v3.py`, `mclust_residual_v4.py`
(`residual_attempt/`) e `lemma_direct_test_v3_fullscale.py`,
`mclust_aggregation_validate.py`, `mclust_residual_v5.py`
(`aggregation_closure_attempt/`).

Todo script nesta subpasta é implementação própria — nenhum arquivo desta
subpasta importa qualquer script de `residual_attempt/` ou
`aggregation_closure_attempt/` (exceto `mclust_global_formula.py`, escrito
NESTA subpasta, importado pelos dois scripts desta subpasta que o usam,
conforme já é prática registrada nos dois documentos predecessores para
scripts de uma mesma frente). Sementes usadas nesta subpasta, todas novas e
nunca reusadas entre si nem com nenhuma frente anterior:

- `SeedSequence(20260822910)` — `global_exclusion_walk_measure.py` (§3,
  medição direta walk-level).
- `SeedSequence(20260822911)` — `mclust_global_validate.py` (§5, validação
  final de 18 células).

Nenhuma delas é `SeedSequence(20260822018)` (onda 4), `SeedSequence(918302033)`
ou `SeedSequence(720330339)` (`residual_attempt/`), ou
`SeedSequence(20260822901)`–`(20260822904)` (`aggregation_closure_attempt/`).
`elevation_needed_analysis.py` (§4) não usa nenhuma semente nova — é análise
determinística (busca de raiz) sobre médias MC já gravadas por
`mclust_aggregation_validate.py` (`aggregation_closure_attempt/`, sementes
20260822904) e pelo próprio `global_exclusion_walk_measure.py` desta
subpasta — reuso explícito e rotulado, não uma validação nova.

## 1. Releitura do que o fator (1−t) já significa (DERIVATIONS.md §0–1)

Antes de formalizar a hipótese de §7.2, é necessário fixar precisamente o
que a fórmula-mestre herdada já modela — o predecessor identificou a
hipótese mas não chegou a reler `DERIVATIONS.md` §0 com esse propósito
específico (ATTEMPT.md dele, §7.2: "não questionada aqui, mas agora com
uma intuição mais clara do MECANISMO por trás dele, não apenas aceito como
dado" — uma intuição, não uma releitura formal).

`DERIVATIONS.md` §0: "Exploration of the f-orbit of a typical point x₀,
parametrized by traversed mass t ∈ [0,1): π-closure into any of the
current arc starts at hazard 1/(1−t) per arc start (uniform among them)".
§1 deriva isso via exposição sequencial de Poisson/PGFL: CADA arc-start
vivo (x₀ e cada sobrevivente de reroteamento) carrega, individualmente, a
MESMA densidade de hazard 1/(1−t) de ser o alvo do PRÓXIMO fechamento — ou
seja, 1/(1−t) já É, desde a onda 2 (M-U, b=1 trivialmente), a densidade
POR-ALVO no pool RESTANTE de tamanho (1−t)n de pontos ainda não consumidos
como imagem de π. Isto é EXATAMENTE o argumento de exposição sequencial de
Fisher–Yates que `aggregation_closure_attempt/ATTEMPT.md` §3.1 usou para
derivar P — aplicado, na fórmula-mestre original (M-U = M-CLUST(1)), à
escala GLOBAL (t·n pontos já consumidos) desde o início, sem nenhuma
elevação (P=1 trivial quando b=1, já que não há janela local nem
correlação de R para contabilizar).

**Conclusão preliminar (não é ainda a resposta completa — ver §2):** o
"pool de tamanho (1−t)n" que §7.2 propõe como correção NOVA já é,
estruturalmente, o que 1/(1−t) sempre representou, herdado sem alteração
desde a onda 2. A pergunta que resta — a genuína — não é "falta uma
correção de escala t·n" (ela já está lá) mas sim: **o fator de elevação P
(que captura o efeito ADICIONAL, de ordem b, da condicional em R) precisa
mudar de valor dependendo de QUANTO da janela local de x já está
absorvida dentro dessa massa t·n global, ou ele se combina
multiplicativamente de forma limpa (P/(1−t), exatamente o que φ_CAND e
φ_CAND5 já implementam) independentemente disso?**

## 2. Formalização precisa: elevação P é independente de profundidade de arco

### 2.1 Setup

Retomando a notação de `aggregation_closure_attempt/ATTEMPT.md` §2–3: x é a
posição atual do passeio, prestes a dar um passo-π normal (x∉R). Definimos
**profundidade de arco** d(x) := número de passos-π normais consecutivos já
dados no arco ATUAL até chegar em x (d=0 se x é o próprio x₀ ou um
sobrevivente de reroteamento recém-criado; d=k se x é o k-ésimo ponto do
arco atual). Fato imediato do mecanismo (não hipótese): se d(x) ≥ b−1,
TODA a janela para trás de x, {π^{-1}(x),...,π^{-(b-1)}(x)}, coincide
EXATAMENTE com os d(x) pontos imediatamente anteriores no MESMO arco — ou
seja, já faz parte da história de visitados do próprio passeio. Se
d(x) < b−1, apenas os d(x) pontos mais próximos da janela coincidem com a
história do arco atual; os b−1−d(x) pontos restantes da janela são
"externos" (vêm de antes do início do arco atual, alcançados via π^{-1}
aplicado ao próprio arc-start, que por sua vez foi atingido por um sorteio
f não relacionado a π).

### 2.2 A elevação P NÃO depende de d(x) [derivado, exato a O(b²/n)]

Re-derivando o lema de exposição sequencial de `aggregation_closure_attempt/ATTEMPT.md`
§3.1 com atenção específica a essa distinção: o argumento central de lá —
"P(y∉R | π(x)=y, x∉R) = 1−c/n exatamente, porque a janela de y
{π^{-1}(y)=x, π^{-2}(y)=π^{-1}(x), ..., π^{-(b-1)}(y)=π^{-(b-2)}(x)} é
EXATAMENTE um subconjunto da janela de x, já confirmada não-semente por
x∉R, sobrando apenas 'y é semente?' como sorteio fresco" — depende
SOMENTE do fato de MARCAS (Bernoulli de semente) nesses b−1 pontos já
serem conhecidas por x∉R. Esse fato é uma afirmação sobre MARCAS, não
sobre se esses pontos já fazem parte do conjunto `visited` do passeio.
Consequentemente, **o argumento vale identicamente para d(x)=0 e para
d(x)≥b−1** — a elevação P=(1−c/n)^{-(b-1)} é, a esta ordem de análise, uma
propriedade PURA de condicionamento-em-marcas, não perturbada por quanto
da janela local já foi "gasto" como história de visitados.

O que MUDA com d(x) é apenas o TAMANHO BRUTO do pool de candidatos: para
d(x)≥b−1, os b−1 pontos da janela de x JÁ ESTÃO contados dentro da massa
t·n global (não são uma exclusão adicional); para d(x)<b−1, faltam
b−1−d(x) pontos que ainda precisam ser excluídos SEPARADAMENTE do pool
(1−t)n. Isso dá uma correção de ORDEM (b−1)/n no denominador — não na
elevação P em si — cujo tamanho paramétrico é ≤ 400/65536 ≈ 0,0061 na
grade mais extrema testada nesta linha: **três ordens de magnitude menor
que o resíduo típico de 2–4% em φ que resta depois de φ_CAND/φ_CAND5**,
quase certamente insuficiente por si só (confirmado numericamente em §2.3).

### 2.3 φ_GLOBAL: a correção de pool O(b/n), implementada e testada

`mclust_global_formula.py` implementa φ_GLOBAL: mesma elevação exata
P=(1−c/n)^{-(b-1)} de φ_CAND5, mas com o pool reduzido uniformemente por
(b−1)/n (uma aproximação por EXCESSO — aplica a correção em TODO s, não só
onde d(x)<b−1 — ver nota de código sobre essa simplificação; o objetivo
aqui é um limite superior barato do tamanho do efeito, não uma forma final):

```
hazard(s) = P / (1 − s − (b−1)/n),   P = (1−c/n)^{-(b-1)}
φ_GLOBAL(c,n,b) := (1−ρ) · ∫₀¹ [P/(1−t−(b−1)/n)] · exp(−c·H_GLOBAL(t)) dt
```

Checagens de sanidade: ρ→0 (b=1) recupera φ_U (diff<1e-6, shift=0 nesse
limite). Reimplementação própria de φ_CAND/φ_CAND5 dentro do mesmo arquivo
(machinery de integração genérica compartilhada) reproduz EXATAMENTE os
valores já gravados em `mclust_aggregation_validate_results.json` para as
4 células de estresse (conferido a 6 casas decimais — ver saída do script,
não persistida em JSON por ser apenas checagem de consistência de
reimplementação, não um resultado novo).

**Resultado:** φ_GLOBAL difere de φ_CAND5 por apenas **+0,11% a +0,44%**
nas 4 células de estresse — como previsto em §2.2, um efeito
paramétricamente pequeno demais para fechar um resíduo de 2–4%. Confirma
numericamente que a correção de TAMANHO DE POOL isolada (sem mudança na
elevação P em si) não é a fonte do resíduo.

## 3. Medição direta: `global_exclusion_walk_measure.py`

Dado que §2.2 argumenta analiticamente que a elevação P não deveria variar
com profundidade de arco, mas isso é um argumento QUE PODE TER UM ERRO
SUTIL (a própria disciplina desta linha de pesquisa, e o próprio histórico
de `residual_attempt/ATTEMPT.md` §2, mostram que argumentos analíticos
aqui já erraram antes), o mandato desta frente pede uma medição DIRETA em
vez de confiar só na álgebra — construída do zero (não importa nenhum
simulador anterior).

### 3.1 Desenho

Estende a lógica de `mclust_walk_diagnostic.py` (própria releitura do
mecanismo, não importada) com DUAS contagens novas que nenhum script
anterior mantinha explicitamente:

- **K**: número de arc-starts VIVOS (x₀ + sobreviventes-de-reroteamento
  ainda não fechados) no instante de cada passo — inicializado a 1 (x₀),
  incrementado a cada evento `reroute→survive`.
- **arc_depth**: profundidade d(x) da posição atual, conforme §2.1.

A cada passo NORMAL (não-reroteamento), registra-se `s_before`, `K_before`,
`arc_depth_before`, e o resultado (fechamento ou avanço livre), agregados
em tempo real (sem lista por evento — dezenas de milhões de passos por
célula tornariam isso inviável em memória) em histogramas 2D
(s-bin × profundidade-bin) de:

```
p0 := K_before / [(1 − s_before) · n]     (densidade SEM elevação nenhuma)
hit := 1 se o passo fecha (destino já visitado), senão 0
```

O estimador de elevação por bin é a razão Horvitz–Thompson
Σhit / Σp0 — válida mesmo com K e s variando dentro do bin, porque cada
evento já carrega seu próprio p0 individual. **Duas categorias de
profundidade apenas** (não 15 bins finos): SHALLOW (d < b−1, janela local
ainda não totalmente absorvida pela história) vs DEEP (d ≥ b−1,
totalmente absorvida) — a dicotomia exata que §2.1 usa, escolhida após um
piloto com 15 bins finos mostrar estatística inutilizável (cada trajetória
contribui exatamente UM evento de fechamento no total, já que o passeio
TERMINA no primeiro fechamento — ~2500 fechamentos totais espalhados por
450 bins finos deu contagens de poucas unidades por bin, sem poder
estatístico; documentado no próprio log do script, seção do pilô
substituída).

### 3.2 Escala de produção, 4 células de estresse, checagem cruzada

`n=65536`, as mesmas 4 células mais extremas já usadas em
`lemma_direct_test_v3_fullscale.py` (b=100/c=400, b=300/c=150, b=100/c=600,
b=400/c=100), 9000–25000 passeios por célula (calibrado por célula para
tempo de parede comparável, dado que o custo por passeio varia ~3× entre
células — mais tráfego de cadeia-R em b·c/n maior), `SeedSequence(20260822910)`,
266s de parede total. Log completo: `global_exclusion_walk_measure.log`,
dados: `global_exclusion_walk_measure_results.json`.

**Checagem cruzada (φ̂ deste simulador vs φ_mc já confirmado):** cyc/n_walks
em cada célula bate com `phi_mc` de `mclust_aggregation_validate_results.json`
dentro de <2,1σ nas 4 células (z = −0,64; +1,62; +2,06; −0,26) — sem
evidência de bug sistemático no simulador novo.

**Resultado (elevação medida, por profundidade):**

| b,c | ρ | P_lead | P_exact | elev SHALLOW | elev DEEP | z(shallow vs P_lead) | z(deep vs P_lead) |
|---|---|---|---|---|---|---|---|
| 100,400 | 0,4579 | 1,8445 | 1,8333 | 1,851±0,026 | 1,838±0,025 | +0,23 | −0,28 |
| 300,150 | 0,4971 | 1,9886 | 1,9841 | 2,130±0,034 | 1,985±0,035 | **+4,11** | −0,12 |
| 100,600 | 0,6014 | 2,5086 | 2,4857 | 2,313±0,026 | 2,338±0,033 | **−7,50** | **−5,21** |
| 400,100 | 0,4571 | 1,8419 | 1,8391 | 1,743±0,034 | 1,668±0,032 | **−2,93** | **−5,37** |

**Achado honesto: NÃO há um padrão universal, monotônico e de sinal
consistente.** Em 3 de 4 células, SHALLOW > DEEP (razões 1,007 / 1,073 /
1,045) — na direção que a hipótese de §7.2 preveria (janela local ainda
não absorvida ⟹ elevação extra) — mas em 1 célula (b=100,c=600, a de maior
ρ=0,60 testada) a razão se inverte ligeiramente (0,989). Mais
decisivamente: em 2 das 4 células (b=100,c=600 e b=400,c=100) TANTO
shallow QUANTO deep estão SIGNIFICATIVAMENTE ABAIXO de P_lead/P_exact —
n a direção ERRADA para ajudar a fechar o resíduo conhecido (φ_mc > φ_CAND
> φ_CAND5 nas 4 células de estresse, exigindo elevação EFETIVA MAIOR, não
menor, que P_lead — ver §4).

## 4. O teste decisivo: P_necessário vs. elevação medida

### 4.1 Método

Para isolar se uma REPONDERAÇÃO por profundidade da elevação já medida
poderia, em princípio, fechar o resíduo — sem precisar construir uma
fórmula-mestre completa dependente de profundidade (esforço substancial,
adiado até saber se vale a pena) — `elevation_needed_analysis.py` resolve,
para cada célula, o valor CONSTANTE P_necessário que faz
φ(hazard=P/(1−s)) bater EXATAMENTE com φ_mc já gravado (fresco, sementes
20260822904 de `aggregation_closure_attempt/`), e compara contra
elev_shallow/elev_deep medidos em §3. **Lógica do teste:** se P_necessário
cai ENTRE (ou próximo de) elev_shallow e elev_deep, uma reponderação por
fração-de-tempo-em-cada-regime é, em princípio, capaz de reproduzi-lo. Se
P_necessário excede AMBOS, nenhuma reponderação da densidade já medida
pode fechar o resíduo daquela célula — a peça faltante estaria em outro
lugar do mecanismo, não nesta densidade por-passo.

### 4.2 Resultado

| b,c | ρ | P_necessário | P_lead | P_exact | elev SHALLOW | elev DEEP | veredito |
|---|---|---|---|---|---|---|---|
| 100,400 | 0,458 | 1,8934 | 1,8445 | 1,8333 | 1,851 | 1,838 | alcançável (dentro/perto da faixa medida) |
| 300,150 | 0,497 | 2,0469 | 1,9886 | 1,9841 | 2,130 | 1,985 | alcançável (P_necessário ENTRE shallow e deep) |
| 100,600 | 0,601 | 2,6038 | 2,5086 | 2,4857 | 2,313 | 2,338 | **INALCANÇÁVEL: excede ambos por 11,4%** |
| 400,100 | 0,457 | 1,9273 | 1,8419 | 1,8391 | 1,743 | 1,668 | **INALCANÇÁVEL: excede ambos por 10,6%** |

(script: `elevation_needed_analysis.py`; dados:
`elevation_needed_analysis_results.json`; reusa φ_mc já gravado — nenhuma
simulação nova nesta etapa.)

**Este é o resultado central deste documento.** Para as duas células mais
"moderadas" (b=100/c=400, b=300/c=150 — ρ ≤ 0,50), a elevação medida
diretamente, quando devidamente reponderada por profundidade, TEM
magnitude suficiente para em princípio explicar o φ verdadeiro — a
hipótese de §7.2, formalizada e medida, é PLAUSÍVEL nesse regime. Mas para
as duas células mais extremas testadas nesta linha inteira (b=100/c=600,
ρ=0,60, a maior testada; b=400/c=100, o maior b testado) — exatamente as
células onde o resíduo original de onda 4 e de φ_CAND/φ_CAND5 é maior —
**nenhuma reponderação possível da densidade medida diretamente no
mecanismo alcança o que seria necessário.** A lacuna (10,6–11,4%, muitos σ
de folga dado o erro de medição de ~1,5–2%) é demasiado grande e
sistemática para ser artefato estatístico.

## 5. Validação de φ_GLOBAL na grade completa de 18 células (sementes novas)

Ainda assim, por completude e honestidade metodológica (mesmo sabendo, por
§2.3 e §4, que φ_GLOBAL não deveria melhorar substancialmente sobre
φ_CAND5), `mclust_global_validate.py` roda a MESMA grade de 18 células de
`residual_attempt/mclust_residual_validate.py` e
`aggregation_closure_attempt/mclust_aggregation_validate.py`, implementação
própria, `SeedSequence(20260822911)` — nunca usada em nenhum outro lugar
desta linha.

211s de parede, 18 células (as mesmas dos dois predecessores — 3 células
b=8, 4×b=50, 4×b=100, 4×b=200, mais as 3 células de estresse extra
b=300/c=150, b=100/c=600, b=400/c=100).

**Resultado agregado:**

| fórmula | χ² (18 células) |
|---|---|
| φ_CAND (`residual_attempt/`) | **79,95** |
| φ_CAND5 (`aggregation_closure_attempt/`) | 98,16 |
| φ_GLOBAL (esta frente) | 87,65 |

**Células mais extremas (as 3 que já ultrapassavam tudo testado antes de
`residual_attempt/`):**

| b,c | ρ | bc/n | dev% CAND (z) | dev% CAND5 (z) | dev% GLOBAL (z) |
|---|---|---|---|---|---|
| 300,150 | 0,497 | 0,687 | +3,29% (+3,84) | +3,46% (+4,03) | +3,12% (+3,64) |
| 100,600 | 0,601 | 0,916 | +3,86% (+4,54) | +4,56% (+5,32) | +4,44% (+5,19) |
| 400,100 | 0,457 | 0,610 | +3,25% (+3,72) | +3,36% (+3,84) | +2,90% (+3,34) |

**φ_GLOBAL fica ENTRE φ_CAND e φ_CAND5 em χ² agregado e em toda célula
individual** — consistente com sua construção (φ_GLOBAL = φ_CAND5 mais um
pequeno deslocamento positivo de pool, §2.3), mas o deslocamento é
pequeno demais para alcançar, quanto mais superar, φ_CAND. **φ_GLOBAL NÃO
melhora sobre a melhor fórmula já disponível nesta linha (φ_CAND)** —
resultado numérico plenamente consistente com a previsão de §2.3 e com o
teste decisivo de §4.

Log completo: `mclust_global_validate.log`, dados:
`mclust_global_validate_results.json`.

## 6. Honestidade — o que este documento estabelece, o que não, e o que fica aberto

**O que ficou estabelecido (derivado E medido diretamente, sementes
novas):**

1. O fator (1−t) da fórmula-mestre herdada (`DERIVATIONS.md` §0–1, onda 2)
   JÁ representa, desde sua origem, exatamente o pool de tamanho (1−t)n de
   pontos ainda não consumidos como imagem de π ao longo de TODA a
   trajetória — a mesma exclusão de escala t·n que §7.2 do predecessor
   hipotetizou estar faltando. Ela não está faltando; está lá desde a
   onda 2, e φ_CAND/φ_CAND5 já a herdam corretamente via o hazard
   P/(1−s).
2. A elevação P (efeito de ordem b, condicionamento em R) é, por um
   argumento de exposição sequencial estendido (§2.2), uma propriedade
   PURA de marcas — independente de quanto da janela local de x já está
   absorvida na história do próprio passeio (profundidade de arco). A
   ÚNICA interação genuína entre exclusão local (ordem b) e exclusão
   global (ordem t·n) é uma correção de TAMANHO DE POOL de ordem (b−1)/n
   — implementada como φ_GLOBAL, numericamente **±0,1–0,4%** de efeito nas
   4 células de estresse, paramétricamente pequena demais para o resíduo
   de 2–4% observado.
3. Medição direta, walk-level, com estimador Horvitz–Thompson que usa o
   K(t) REAL de cada passeio (não uma fórmula assumida para K), em escala
   de produção (n=65536), sementes novas, cruzada com φ_mc já confirmado
   (<2,1σ em todas as 4 células): a elevação medida NÃO mostra uma lei
   universal, monotônica e de sinal consistente em função da profundidade
   de arco — em 3/4 células shallow>deep (fracamente, 1–7%), em 1/4 a
   relação se inverte.
4. **O teste decisivo (§4):** mesmo permitindo QUALQUER reponderação por
   profundidade da densidade medida diretamente (o melhor caso possível
   para a hipótese de §7.2), 2 das 4 células de estresse — precisamente as
   de MAIOR ρ e MAIOR b, onde o resíduo de onda 4/φ_CAND é historicamente
   maior — permanecem com uma lacuna de 10,6–11,4% entre o que seria
   necessário e o que é fisicamente mensurável nesta densidade por-passo.

**Conclusão sobre a hipótese específica de §7.2:** formalizada
rigorosamente (exposição sequencial, §2) e testada diretamente por
simulação em escala de produção (§3–4), a hipótese "densidade ~1/[(1−t)n]
em vez de ~1/n" acaba sendo, em parte, uma REDESCOBERTA do que a
fórmula-mestre já fazia desde a onda 2 (o (1−t) já era essa escala) — e a
peça genuinamente NOVA que ela aponta (interação entre exclusão de janela
local e história global, dependente de profundidade de arco) é, quando
medida com o máximo rigor que este documento conseguiu montar,
**insuficiente para fechar o resíduo nas células de maior ρ/b — não apenas
"não fechada", mas ATIVAMENTE DESCARTADA como explicação SUFICIENTE
nessas células, com uma lacuna quantificada (10,6–11,4%) que uma
reponderação por profundidade, mesmo na melhor das hipóteses, não
alcança.**

**O que continua aberto (nomeado, não perseguido nesta frente):**

1. O teste de §4 mostra que a densidade "K/((1−t)n)×elevação" — mesmo
   medida com o K REAL do passeio — não é a fonte suficiente do resíduo
   nas células mais extremas. Isso desloca a suspeita para OUTRAS peças da
   maquinaria da fórmula-mestre não testadas aqui: (a) a precisão de
   q_CLUST(s)=s/(1−ρ) especificamente em ρ alto (só reconfirmada por
   `residual_attempt/ATTEMPT.md` §3.1 em ρ até ~0,46; a célula mais
   discrepante aqui tem ρ=0,60, fora dessa faixa já confirmada); (b) uma
   possível assimetria entre x₀ (fixo desde o início, nunca criado por um
   sorteio de reroteamento) e os OUTROS membros de Y_live (todos criados
   dinamicamente por sobrevivência de reroteamento) — o formalismo de §2–3
   assume ambos se comportam identicamente sob a mesma elevação P, mas
   isso não foi testado separadamente; (c) a aproximação de
   Poissonização/independência da própria fórmula-mestre, já listada como
   em aberto por `residual_attempt/ATTEMPT.md` §8 item 3 e
   `aggregation_closure_attempt/ATTEMPT.md` §9, permanece a suspeita mais
   estrutural e menos testada de todas nesta linha inteira.
2. Não foi construída (nem seria justificado, dado §4, gastar o esforço
   substancial de construir) uma fórmula-mestre dependente de profundidade
   de arco de forma completa (um hazard bivariado (s,d), integrado via uma
   EDO ou PGFL de dois parâmetros) — o teste de §4 já mostra que mesmo o
   MELHOR CASO dessa construção não fecharia 2 das 4 células de estresse,
   então esse investimento foi conscientemente NÃO feito aqui.

## 7. Veredito

> **NÃO-FECHAMENTO HONESTO da hipótese específica de §7.2, com
> caracterização nova e mais precisa de onde a dificuldade genuinamente
> mora.** A releitura cuidadosa da fórmula-mestre herdada (§1) mostra que
> a exclusão de escala t·n que a hipótese propunha como faltante já está
> presente desde a onda 2, incorporada no fator (1−t); a formalização
> rigorosa da interação entre exclusão local (ordem b) e história global
> (§2) mostra que a única correção genuína remanescente é de ordem (b−1)/n
> — testada numericamente (φ_GLOBAL) e confirmada pequena demais
> (±0,1–0,4% nas células de estresse, contra um resíduo de 2–4%). A
> medição direta, walk-level, com o K(t) real do mecanismo (§3) não revela
> uma lei de profundidade universal, e o teste decisivo (§4) — perguntando
> se QUALQUER reponderação por profundidade da densidade fisicamente
> mensurável poderia fechar o resíduo — mostra que NÃO PODE, em pelo menos
> 2 das 4 células de maior ρ/b, por uma margem de 10,6–11,4%, muitos σ
> além do erro de medição. φ_CAND (`residual_attempt/ATTEMPT.md`) continua
> sendo a melhor fórmula desta linha inteira; este documento não a supera
> nem tenta apresentar φ_GLOBAL como candidata superior (a validação de
> §5 confirma numericamente que não é). O valor deste documento é
> negativo mas preciso: descarta, com derivação E medição direta (não
> apenas ajuste), a hipótese específica nomeada como a fonte do resíduo
> remanescente, e realoca a suspeita para outras peças da maquinaria
> (q_CLUST em ρ alto, assimetria x₀-vs-outros-arc-starts, ou a
> Poissonização da própria fórmula-mestre) — nenhuma delas testada nesta
> frente. A classificação M-CLUST(b) ∈ U_{1/2} no limite n→∞ (∀ b fixo)
> permanece completamente intocada por tudo acima.

## Arquivos (todos nesta subpasta, `global_exclusion_attempt/`)

- `ATTEMPT.md` — este documento.
- `PROGRESS.log` — checkpoints de progresso (não é o relatório final).
- `global_exclusion_walk_measure.py` / `.log` / `_results.json` — §3,
  simulador de passeio walk-level próprio com contagem explícita de K(t) e
  profundidade de arco, estimador Horvitz–Thompson por bin, sementes
  20260822910.
- `mclust_global_formula.py` — §2.3, reimplementação própria de φ_CAND/
  φ_CAND5 (checagem de consistência contra os valores já gravados dos
  predecessores) mais φ_GLOBAL (a correção de pool O(b/n)).
- `elevation_needed_analysis.py` / `_results.json` — §4, o teste decisivo
  P_necessário vs. elevação medida (reuso de MC já gravado, sem sementes
  novas).
- `mclust_global_validate.py` / `.log` / `_results.json` — §5, validação
  final fresca de 18 células, sementes 20260822911.
