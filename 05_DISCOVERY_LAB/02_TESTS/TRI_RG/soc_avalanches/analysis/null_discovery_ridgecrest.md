# Descoberta adversarial de nulos — `DISC-TRI-RG-001` / `soc-avalanches` / Ridgecrest

**Papel:** agente de destruição convencional (Extensão de Metodologia 5,
`05_DISCOVERY_LAB/00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`).
**Alvo:** achado de `05_DISCOVERY_LAB/02_TESTS/TRI_RG/soc_avalanches/analysis/result_ridgecrest.json`,
variante `segment_selection_robustness_50pct_split` — `tau_pre=4,090`,
`tau_post=2,358`, `Delta_tau=-1,733`, `p_bootstrap_tau=0,0` (primário),
`p_tau=0,32` (Poisson, secundário).

## Veredito

**O achado NÃO sobrevive como sinal novo de "avalanche/SOC" ou candidato a
observação discriminante para Tamesis. Ele se reduz inteiramente a física
de decaimento de réplicas já conhecida (Omori-Utsu, décadas de literatura),
manifestada aqui através de uma sensibilidade mundana e mecânica do próprio
pipeline (binagem de largura fixa `lambda`) à taxa LOCAL de eventos — não a
uma diferença estrutural de "criticalidade" entre as duas sequências.**

Reproduzo, com `p_bootstrap_tau=0,0` idêntico ao do achado real, o MESMO
sinal (mesmo sinal, magnitude comparável ou maior) **inteiramente dentro da
sequência de réplicas do M7,1** — sem qualquer comparação PRE/POST, sem
qualquer referência ao M6,4, só cortando a própria janela POST em dois
subintervalos de tempo. Isso demonstra que o teste primário (bootstrap
pareado de `tau`) não distingue "estrutura SOC real" de "artefato de
variação de taxa local dentro de uma única sequência de Omori" — ele é
significativo nos dois casos igualmente.

## O que já estava certo no design original

A nota de metodologia (`METHODOLOGY_NOTE.md`) já identificou a maior parte
dos riscos corretos a priori: `lambda` fixo calculado do fluxo combinado
(para não deixar uma mudança pura de taxa induzir mecanicamente uma
diferença de estrutura), correção de `Mc` por máxima curvatura para
mitigar STAI, teste bicaudal, e um teste secundário de substituto Poisson
que, corretamente, NÃO deu significativo (`p=0,32`). O problema não é falta
de disciplina — é que a mitigação de `lambda` fixo protege contra o caso
TRIVIAL (recalcular `lambda` por segmento) mas não contra o caso mais sutil
que efetivamente ocorre aqui, demonstrado abaixo.

---

## Ataque 1 (rota mais provável, CONFIRMADA): dependência de `tau` à taxa
local de eventos, mecanismo de Omori-Utsu, sem nenhum ingrediente novo

### 1a. O confundidor identificado pelo agente original é preciso, e mais grave do que parecia

Reconstruí os dois segmentos de robustez diretamente do catálogo bruto
(`ridgecrest_catalog.csv`, corte `Mc_final=1,35`) e confirmei bit a bit os
números do `result_ridgecrest.json` (`lambda=62,449677`, `n_events`,
`t_min`/`t_max` idênticos até a casa decimal).

- **PRE-robustez:** 2019-07-05 03:56:05 → 2019-07-06 03:17:13 UTC (23,35h).
  Começa **10,37h DEPOIS do M6,4** (2019-07-04 17:33:49 UTC) e termina
  exatamente no instante do M7,1. Está **inteiramente dentro da cauda
  declinante da sequência de réplicas do próprio M6,4** — a fase de taxa
  mais baixa dessa sequência, não sismicidade de fundo quiescente.
- **POST-robustez:** 2019-07-06 03:19:53 UTC → 2019-07-10 19:08:18 UTC
  (4,66 dias). Começa exatamente no M7,1 e cobre os primeiros 4,66 dias —
  **a fase mais densa/de taxa mais alta** da sequência de réplicas do M7,1.

Ou seja: o "achado" compara a **cauda de taxa baixa** de uma sequência de
réplicas menor contra o **início de taxa alta** de uma sequência de
réplicas maior. Isso não precisa de nenhuma diferença de magnitude entre
M6,4 e M7,1 para gerar um `Delta_tau` — precisa só de decaimento de Omori,
que TODA sequência de réplicas tem.

### 1b. Teste direto: o mesmo efeito aparece DENTRO da sequência do M7,1 sozinha

Dividi a janela POST-robustez (M7,1, 4,66 dias) em duas: um subintervalo
INICIAL com a MESMA duração exata do segmento PRE (23,35h, a maior taxa
local do próprio M7,1) e um subintervalo TARDIO com o restante (88,45h,
taxa mais baixa, mais parecida com a taxa de PRE). Rodei
`soc_common.analyze_segment` (importado sem modificação) com o MESMO
`lambda` compartilhado usado no achado real:

| segmento | duração | mu (eventos/s) | n_avalanches | tau | n_tail | xmin |
|---|---|---|---|---|---|---|
| POST-inicial (0–23,35h do M7,1) | 84.068s | 0,0385 | 109 | **2,501** | 44 | 21,0 |
| POST-tardio (23,35h–4,66d do M7,1) | 318.438s | 0,0114 | 1222 | **3,512** | 227 | 5,0 |

`Delta_tau(tardio - inicial) = +1,011`, teste de bootstrap pareado
(mesma função `paired_bootstrap_tau_test` do pipeline primário) dá
**`p_bootstrap_tau = 0,0`**, CI95 `[0,385; 1,549]` — tão "significativo"
quanto o achado real, e mesmo SINAL qualitativo (taxa local mais baixa →
`tau` mais alto), **sem nenhuma comparação entre sequências diferentes**.

### 1c. Confirmação sistemática: `tau` acompanha a taxa local em toda a sequência do M7,1

Escaneei a janela POST completa (`post_primary`, 60 dias, 13.768 eventos)
em 10 blocos consecutivos de duração igual, com o mesmo `lambda=62,45`:

| dias desde o M7,1 | mu (eventos/s) | n_avalanches | tau | n_tail |
|---|---|---|---|---|
| 0,00 | 0,01505 | 1745 | 2,458 | 485 |
| 5,98 | 0,00395 | 1337 | 4,499 | 152 |
| 11,96 | 0,00210 | 873 | 4,551 | 165 |
| 17,94 | 0,00152 | 665 | 4,481 | 93 |
| 23,92 | 0,00095 | 441 | 7,278 | 47 |
| 29,90 | 0,00073 | 350 | 8,000 | 24 |
| 35,88–53,82 | 0,0004–0,0007 | 204–343 | 3,37–5,18 | poucos (n baixo, ruidoso) |

Correlação de Pearson `(mu, tau)` = **-0,527**; `(log mu, tau)` = **-0,471**
— negativa e substancial, inteiramente dentro de UMA sequência homogênea,
sem qualquer referência ao M6,4. O bloco inicial (taxa mais alta) reproduz
quase exatamente `tau_post=2,36` do achado real; blocos de taxa baixa
alcançam e ultrapassam `tau_pre=4,09` (chegando a 7-8 nos blocos de menor
`n`, onde ruído de amostra pequena — ver Ataque 2 — também contribui).

### 1d. Literatura

Confirmado por busca (não é conhecimento novo): a lei de Omori-Utsu
`R(t) = K/(c+t)^p` descreve exatamente esse declínio de taxa por lei de
potência após qualquer evento principal, com `p` tipicamente 0,9–1,5 e
variando de sequência a sequência (Utsu, Ogata & Matsu'ura 1995, *The
Centenary of the Omori Formula*). Incompletude de curto prazo (STAI) é
tema ativo e documentado na literatura sismológica precisamente na janela
inicial pós-mainshock (Hainzl 2016 *SRL*; Helmstetter, Kagan & Jackson
2006), com fórmulas publicadas de magnitude de detecção dependente do
tempo desde o evento principal, ex. `m_det(t,M) = M - 4,5 - 0,75 log10(t)`.
Isso não muda o veredito (ver Ataque 5), mas confirma que "taxa/densidade
de réplicas varia por ordens de magnitude ao longo de uma única sequência,
por um mecanismo já conhecido há décadas" é exatamente o pano de fundo
correto para o que os testes 1b/1c acima demonstram numericamente.

**Conclusão do Ataque 1:** o pipeline de avalanches, com `lambda` fixo,
converte variação de taxa LOCAL (não média-de-segmento) em variação de
`tau` — um artefato mecânico do método de binagem de largura fixa quando
aplicado a um processo com taxa fortemente não estacionária, que é
exatamente o que decaimento de Omori-Utsu garante em qualquer sequência de
réplicas. PRE cai numa fase de taxa baixa (cauda do M6,4); POST-robustez
cai numa fase de taxa alta (início do M7,1). Nenhuma física nova é
necessária.

---

## Ataque 2 (rota testada, mas REJEITADA como explicação isolada): viés de
amostra pequena / MLE

Testei diretamente se o desequilíbrio de tamanho de cauda (`n_tail=60` em
PRE vs `n_tail=426` em POST) é, por si só, suficiente para produzir a
diferença observada — reamostrando a PRÓPRIA população de avalanches de
POST (mesmo processo gerador, por construção) para o tamanho de PRE:

- **2000 reamostras sem reposição** de POST-robustez (1310 avalanches) para
  `n=327` (tamanho exato de PRE), refit completo via
  `soc_common.fit_powerlaw_clauset` (mesma busca de `xmin` por KS):
  `tau` médio = **2,328** (desvio 0,158), muito próximo do `tau_post=2,358`
  real. Apenas **0,05%** das 2000 reamostras alcançam `tau >= 4,090`
  (o `tau_pre` real).
- Ainda mais direto: fixando `xmin=5` (o próprio `xmin` selecionado para
  PRE) e sorteando `n=60` (o `n_tail` exato de PRE) do pool de POST com
  `s>=5`: `tau` médio = **2,360** (desvio 0,164). **0 em 2000** reamostras
  alcançam `tau >= 4,090`, e **0 em 2000** alcançam sequer o limite
  inferior do IC95% de bootstrap de PRE (3,50).

**Isso mata a explicação de "puro ruído de MLE em amostra pequena"**: dado
o MESMO processo gerador (a própria população de avalanches de POST),
amostras do tamanho de PRE não produzem `tau~4`. A diferença de `n`
sozinha não é a causa — a causa é que PRE e a fatia POST-inicial vêm de
regimes de taxa local genuinamente diferentes (Ataque 1), não de ruído de
amostragem em torno de um único `tau` verdadeiro compartilhado.

Isso é um resultado adversarial HONESTO no sentido oposto ao esperado pela
tarefa: a rota #2 sugerida pela tarefa (efeito de tamanho de amostra) foi
testada e **não** é a explicação. A rota #1 (Omori-Utsu/taxa local) é.

---

## Ataque 3: a divergência primário/secundário É o sinal de alerta —
números

- Bootstrap pareado (primário): `Delta_tau_boot` média `-1,773`, desvio
  `0,402`, CI95 `[-2,646; -1,118]`, `p=0,0`. Este teste só usa a incerteza
  de reamostragem DENTRO de cada segmento observado — não testa contra
  nenhum processo gerador alternativo.
- Substituto Poisson (secundário, casado em taxa média por segmento):
  `Delta_tau` médio do nulo = `0,413`, desvio `1,744`. `z = (Delta_tau_real
  - media_nulo)/desvio = (-1,733 - 0,413)/1,744 ≈ -1,23`, `p=0,32`
  (bicaudal) — nada extremo.
- O Ataque 1b reproduz `p_bootstrap_tau=0,0` usando o MESMO teste primário
  aplicado a um recorte que é, por construção, 100% física de réplicas
  convencional (dentro do M7,1). Isso prova empiricamente que
  `p_bootstrap_tau=0,0` **não discrimina** estrutura SOC real de artefato
  de taxa local — ele é significativo nos dois casos.
- O teste Poisson secundário, mesmo sendo o nulo "errado" para sismologia
  (homogêneo, não ETAS/Omori), já capturou parcialmente o problema
  (`p=0,32`, não significativo) precisamente porque ele pelo menos casa a
  taxa MÉDIA do segmento — mas não a não-estacionariedade INTERNA da taxa,
  que é onde o efeito realmente mora (Ataque 1c mostra a correlação
  `tau`-`mu` LOCAL, não só a taxa média do segmento inteiro).

**Conclusão:** a divergência não é ambiguidade estatística menor — é
exatamente o padrão esperado quando o teste primário é sensível a um
confundidor de taxa local que o secundário (mesmo imperfeito) já começa a
enxergar.

---

## Ataque 4: a variante primária falhou por completo — o achado só existe
na variante de robustez

- Variante **primária** (sem truncamento de 50%): PRE tem só 9 avalanches,
  `tau_fit.reason = "insufficient_data"`, `tau_pre = None`,
  `delta_tau = None`. **Nenhum resultado existe** nessa variante.
- Variante de robustez de `lambda` DENTRO da própria variante de 50%-split
  já é inconsistente em magnitude: `lambda_div2` dá `Delta_tau=-2,917`;
  `lambda_x2` dá `Delta_tau=-0,591`. Mesmo sinal em todas as 3
  variantes de `lambda` testadas, mas variação de quase 5x na magnitude —
  compatível com um efeito que depende fortemente de exatamente qual
  janela/escala de tempo você mede (Ataque 1), não com uma quantidade
  fisicamente estável.
- Diferente do "vazamento" clássico (escolher a posteriori a variante mais
  favorável), a regra dos 50%-mais-recentes/próximos já estava fixada A
  PRIORI no `METHODOLOGY_NOTE.md` gap (d), reaproveitada sem modificação de
  candidatos anteriores da trilha — não foi inventada depois de ver o
  resultado. Mas isso não resolve o problema de fundo: o "achado" só
  aparece quando a amostra é reduzida a EXATAMENTE a janela de taxa mais
  baixa possível de PRE (cauda do M6,4) contra a janela de taxa mais alta
  possível de POST (início do M7,1) — a variante primária, que usa a
  janela PRE completa (2 dias, dominada em maior parte pela MESMA cauda de
  taxa baixa, mas com mais amostra), já não consegue nem gerar um `tau_pre`
  definido. Isso é consistente com — não independente de — o mecanismo do
  Ataque 1: a variante primária tem menos avalanches justamente porque boa
  parte da janela PRE completa está na fase de taxa mais baixa ainda.

---

## Ataque 5: viés de catálogo / STAI / densidade de rede

Já mitigado no desenho original (corte único `Mc_final=1,35 =
max(Mc_PRE,Mc_POST)+0,2`, calculado por máxima curvatura). Testei se esse
corte, calculado sobre os segmentos PRE/POST INTEIROS (2 dias vs 60 dias),
poderia estar mascarando incompletude residual especificamente na janela
inicial de POST-robustez (as primeiras horas pós-M7,1, onde STAI é mais
grave). Direção do efeito: STAI faz o catálogo **perder eventos pequenos**
justamente na janela de maior atividade — isso tenderia a **subestimar**
`mu` real de POST-inicial e a **reduzir** o tamanho aparente de avalanches
ali, o que enviesaria `tau_post` para CIMA (mais perto de `tau_pre`), não
para baixo. Ou seja, STAI residual, se existir, tende a ATENUAR a
diferença observada, não a criá-la — não é uma explicação alternativa que
"resgate" o achado nem uma que o destrua adicionalmente; é consistente com
o Ataque 1 já ser suficiente e talvez até conservador.

---

## Síntese e recomendação

1. **O achado não é identificável em relação a um modelo concorrente
   nomeado e real** (Seção 1 de `METHODOLOGY_EXTENSIONS.md`): decaimento de
   Omori-Utsu, aplicado através deste pipeline de binagem de largura fixa,
   já produz `Delta_tau` do mesmo sinal, magnitude comparável, e mesmo
   `p_bootstrap_tau=0,0` **inteiramente dentro de uma única sequência de
   réplicas conhecida**, sem qualquer transição de regime. `P(D|Omori-Utsu
   convencional) approx P(D|Tamesis)` — a condição de identificabilidade
   falha.
2. A explicação especificamente sugerida pela tarefa como "mais provável"
   (rota 1, Omori-Utsu/dependência de taxa) é CONFIRMADA numericamente, de
   forma direta e reproduzível, com o próprio pipeline do laboratório.
3. A explicação de tamanho de amostra (rota 2) foi testada e **rejeitada**
   como causa suficiente — registrado aqui por rigor adversarial simétrico,
   não é uma defesa do achado.
4. Recomendação para `TEST_QUEUE.yaml`: `DISC-TRI-RG-001`/`soc-avalanches`
   em sismologia deve ser rotulado **não sobrevive à descoberta adversarial
   de nulos** — reduzido a "física de réplicas de Omori-Utsu já conhecida,
   manifestada como sensibilidade de `tau` à taxa local de eventos sob
   binagem de largura fixa", não avança para o Gate de Replicação neste
   domínio. Se o candidato `soc-avalanches` for perseguido adiante, exigiria
   no mínimo (a) um nulo ETAS subcrítico ajustado (já reservado como
   escalada condicional no `METHODOLOGY_NOTE.md`) que reproduza a
   trajetória `tau(t)` observada no Ataque 1c, e (b) uma estatística que
   controle explicitamente para taxa LOCAL (não só taxa média do segmento)
   antes de qualquer novo pré-registro.
5. O resultado em flares solares GOES (`result_goes_flares.json`) não foi
   reexaminado aqui — está fora do escopo desta tarefa (Ridgecrest), mas o
   mesmo mecanismo (`lambda` fixo + taxa local não-estacionária) é uma
   hipótese natural a testar lá também, dado que erupções solares também
   têm perfis de atividade fortemente não estacionários dentro do ciclo
   solar.

## Reprodutibilidade

- `soc_common.py` foi importado sem modificação (`git diff` limpo,
  confirmado abaixo).
- Segmentos reconstruídos diretamente do catálogo bruto
  (`data/ridgecrest_catalog.csv`) batem byte-a-byte com
  `result_ridgecrest.json` (`lambda`, `n_events`, `t_min`, `t_max`).
- Números completos desta análise em
  `null_discovery_ridgecrest.json` (mesmo diretório).
- Scripts usados (não versionados, scratch de sessão):
  reconstrução de segmentos + Ataques 1b, 1c, 2 — disponíveis por
  referência ao histórico desta sessão caso um agente futuro precise
  reexecutar; a lógica está integralmente descrita acima com números
  suficientes para reprodução independente sem depender dos scripts em si.
