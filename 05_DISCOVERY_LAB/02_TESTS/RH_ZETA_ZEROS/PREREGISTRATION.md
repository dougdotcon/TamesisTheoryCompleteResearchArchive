# Pré-registro: runs de gaps moderados consecutivos entre zeros reais de ζ(s) — correlação sequencial vs. reordenação aleatória

**Status:** LOCKED
**Data de criação:** 2026-08-12
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-12 (Claude Code)
**Test ID:** `DISC-RH-ZERO-GAP-RUNS-001` (sub-teste de `DISC-RH-REAL-001`)
**Commit em que foi travado:** ver histórico git do commit que introduz este arquivo.

> Preenchido e commitado ANTES de rodar o teste de permutação sobre o
> dado real. A Fase 0 (`PHASE0_TRIAGE_SUMMARY.md`) já leu os arquivos de
> dado para fins de formato/proveniência e já computou estatísticas
> exploratórias (correlação de pares, espaçamento médio, correlação
> serial entre gaps consecutivos) — isso é formulação de hipótese
> permitida (`AGENTS.md` passo 2), não uma violação de lock, porque
> nenhuma dessas estatísticas exploratórias é a estatística de teste
> travada abaixo, e o critério de falsificação foi fixado ANTES de
> qualquer cálculo com essa estatística específica.

## 0. Motivação e o que este teste NÃO é

O item 9 do levantamento de literatura (`PHASE0_TRIAGE_SUMMARY.md`) é uma
questão explicitamente **em aberto** (arXiv:2412.15481, dez/2024): existem
infinitos runs de `r` gaps consecutivos normalizados todos `≥ c` (c
pequeno fixo)? Uma afirmação "infinitos" não é testável nem falsificável
com dado finito — nenhum teste aqui confirma ou refuta essa conjectura.

Este pré-registro testa uma **pergunta proxy, genuinamente falsificável,
motivada por ela**: a sequência real e ordenada por altura de gaps
normalizados entre zeros de ζ(s) mostra correlação sequencial de curto
alcance (mais runs de gaps consistentemente não-pequenos do que se
esperaria se a mesma coleção de valores de gap fosse reordenada
aleatoriamente)? Isso testa se a estrutura de repulsão de nível GUE já
observada na Fase 0 (`PHASE0_TRIAGE_SUMMARY.md`, item 1: supressão de
~10× na densidade de pares perto de u=0) tem um efeito detectável na
formação de runs — não é uma tentativa de estabelecer a conjectura
"infinitos runs" em si.

## 1. Hipótese exata

**H:** a sequência real, ordenada por altura, dos gaps normalizados entre
zeros consecutivos de ζ(s) contém MAIS runs de `r` gaps consecutivos
todos `≥ c` do que a distribuição nula obtida reordenando aleatoriamente
(permutando) o mesmo multiconjunto de valores de gap — assinatura de
correlação sequencial de curto alcance (repulsão de nível), além do que a
distribuição marginal dos gaps sozinha implicaria.

**Motivação quantitativa (Fase 0, exploratória, computada antes deste
lock mas não constituindo o teste em si):** correlação de Pearson entre
gaps normalizados consecutivos na amostra `zeros1.txt` = **−0,357**
(correlação negativa forte) — gaps pequenos tendem a ser seguidos por
gaps maiores, e vice-versa. Isso motiva a direção da hipótese (mais runs
"todos ≥ c" no dado real do que no nulo aleatório), mas a estatística de
teste travada abaixo é uma coisa diferente (contagem de runs, não
correlação de Pearson) — a correlação de Pearson NÃO é reusada como
estatística de decisão.

## 2. Fonte de dado

- Dataset primário: `data/zeros1.txt` (100.000 primeiros zeros reais de
  ζ(s), Odlyzko) — mesma proveniência já documentada em
  `data/PROVENANCE.md`, reaproveitada sem modificação.
- Dataset secundário (checagem de generalização, ver Seção 4): `data/zeros3.txt`
  (10.000 zeros próximos ao zero #10¹², regime de altura muito diferente
  — γ≈2,68×10¹¹ vs. γ até ~75.000 no primário). **Nota de transparência:**
  o conteúdo bruto de `zeros3.txt` já foi inspecionado nesta sessão
  (cabeçalho e amostra de valores, para fins de formato/proveniência,
  documentado em `data/PROVENANCE.md`) — isto NÃO é um holdout selado no
  sentido do Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`), é um
  dataset secundário já conhecido, declarado explicitamente como checagem
  de generalização informativa, não como parte do critério de decisão
  primário.
- Nenhum novo download necessário — ambos já verificados e commitados
  (Fase 0).

## 3. Modelo nulo / hipótese concorrente

**Nulo (reordenação aleatória / exchangeabilidade):** os 99.999 valores
de gap normalizado observados em `zeros1.txt` não têm nenhuma estrutura
sequencial além de sua distribuição marginal — ou seja, qualquer ordem
dos mesmos valores é igualmente provável. Sob este nulo, a contagem de
runs de `r` gaps consecutivos `≥ c` tem a mesma distribuição
(computável por permutação) independente da ordem real de altura.

Este é o "modelo concorrente nomeado" desta trilha (Methodology
Extensions §1) — não há teoria física concorrente aqui (esta é pesquisa
matemática pura, sem conteúdo Tamesis), então o modelo concorrente
correto é o nulo estatístico padrão para ausência de estrutura
sequencial.

## 4. Estatística de teste

Grade pré-declarada de 6 combinações: `c ∈ {0,10; 0,20; 0,30}` × `r ∈ {2; 3}`.

Para cada combinação `(c, r)`:
1. **Estatística observada:** contar o número de posições `i` (janelas
   sobrepostas permitidas) tais que `gap[i], gap[i+1], ..., gap[i+r-1]`
   são todos `≥ c`, na sequência real `zeros1.txt` ordenada por altura.
2. **Distribuição nula:** gerar 10.000 permutações aleatórias
   independentes do mesmo multiconjunto de 99.999 valores de gap
   (`numpy.random.default_rng(seed=20260812)`), recalcular a mesma
   contagem de runs em cada permutação.
3. **p-valor (uma cauda, direção pré-registrada):**
   `p = (1 + #{permutações com contagem_nula ≥ contagem_real}) / (10.000 + 1)`
   — testa se a contagem real é anormalmente ALTA frente ao nulo
   (direção prevista pela motivação da Seção 1).

## 5. Critério de falsificação

- **Célula individual "suporta H":** `p < 0,05/6 ≈ 0,00833` (correção de
  Bonferroni para as 6 combinações) NA direção prevista (contagem real >
  distribuição nula).
- **Célula individual "não suporta H":** `p ≥ 0,00833`.
- **Célula individual "resultado inverso" (surpresa a ser reportada
  proeminentemente, não escondida):** contagem real significativamente
  MENOR que o nulo (p simétrico do lado oposto < 0,00833) — indicaria
  correlação sequencial na direção OPOSTA à motivada pela Seção 1.
- **Veredito agregado pré-declarado sobre a grade de 6 células:**
  - `STRONG_SUPPORT`: ≥5 das 6 células "suportam H" na direção prevista.
  - `PARTIAL_SUPPORT`: 2-4 células suportam H, nenhuma na direção
    inversa.
  - `NO_SUPPORT`: 0-1 células suportam H.
  - `INVERSE_SIGNAL`: qualquer célula mostra o resultado inverso
    significativo — reportado independentemente do veredito agregado
    acima, nunca reinterpretado como "não suporta" apenas.
- Nenhuma reformulação da grade, dos limiares, ou do critério de
  agregação é permitida após ver os resultados.

## 6. Correção para comparações múltiplas

Seis comparações pré-declaradas (3 valores de `c` × 2 valores de `r`),
correção de Bonferroni aplicada (limiar 0,05/6). O dataset secundário
(`zeros3.txt`, Seção 4) roda a MESMA grade de 6 células mas é reportado
separadamente, explicitamente rotulado como informativo/generalização —
não soma às 6 comparações primárias nem exige correção adicional própria
além da mesma correção de Bonferroni aplicada de forma independente a
ele.

## 7. O que NÃO está sendo testado

- Isto NÃO testa nem confirma/refuta a conjectura de runs infinitos de
  arXiv:2412.15481 — essa afirmação "infinitos" não é testável com dado
  finito. Um resultado positivo aqui é evidência de correlação
  sequencial de curto alcance detectável na amostra estudada, não prova
  de existência infinita de runs.
- Isto NÃO testa, confirma, ou refuta a Hipótese de Riemann.
- Isto NÃO tem nenhum conteúdo Tamesis-específico — é pesquisa matemática
  pura sobre `riemannZeta` real, motivada pelo caso Anthropic, sem
  relação com nenhuma tese do `01_TAMESIS_CORE`.
- Um resultado aqui, mesmo se `STRONG_SUPPORT`, não é uma alegação de
  descoberta matemática nova — a correlação sequencial de curto alcance
  entre gaps de zeros de zeta já é conhecida na literatura GUE
  (Montgomery, Odlyzko); este teste verifica se ela é detectável nesta
  amostra específica com este método específico, como validação de
  ferramental e como base para uma pergunta mais afiada depois, não como
  resultado publicável em si.
- Nenhum resultado aqui é promovido a `04_FORMAL_RESEARCH_LAB` sem
  primeiro sobreviver ao Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`)
  — e mesmo assim, por ser um achado matemático sobre estatística
  empírica de dado finito, não sobre uma afirmação demonstrável em Lean,
  a promoção não é automática (ver `RESEARCH_PIPELINE.md` sobre a
  assimetria entre achados empíricos e achados matematicamente
  demonstráveis).

---

## [Preenchido depois da análise] Resultado

## [Preenchido depois da reexecução adversarial] Veredito adversarial
