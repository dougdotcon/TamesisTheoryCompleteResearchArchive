# Pré-registro — frente C `u12-generalization-u-alpha` (onda 3)

**Linha:** DISC-CORE-NUMERICS-001. **Governança:** DISC-DEC-015.
**Data/hora de gravação:** 2026-08-22T02:07Z — gravado ANTES de qualquer
derivação registrada e de qualquer execução numérica desta frente
(ordem verificável por timestamps dos arquivos).

## Pergunta central

O resultado consolidado das ondas 1–2 (DISC-DEC-014, confirmado
adversarialmente em 4 superfícies): para o ensemble u12 (permutação
uniforme de [n]; cada ponto redirecionado independentemente com
prob. c/n para destino uniforme), φ_∞(c) = ∫₀¹ e^{−ct²} dt, com cauda
(√π/2)·c^{−1/2}. Esta frente pergunta:

1. **Por que o expoente é exatamente 1/2?** (qual ingrediente do
   mecanismo o produz);
2. **Que família de mecanismos de perturbação produz que expoentes?**
   (classes U_α: mecanismo → φ_∞ → expoente de cauda α);
3. O 1/2 é **robusto** (classe grande) ou **frágil** (específico do
   destino uniforme)? Existe mecanismo **natural** com α ≠ 1/2?

## Declaração de estado inicial (honestidade)

Antes de gravar esta nota, o agente desta frente esboçou EM PAPEL (sem
nenhuma execução numérica) a generalização do processo de exploração da
onda 2 para probabilidade de morte genérica q(s), e as contas de
primeira ordem (K=1) dos mecanismos abaixo. Nenhum número novo foi
computado; os únicos números vistos são os públicos das ondas 1–2.
As derivações completas serão registradas em `DERIVATIONS.md` DEPOIS
desta nota e ANTES de qualquer simulação; os alvos numéricos exatos
(quadraturas das fórmulas derivadas) serão gravados em
`predictions.json` ANTES de qualquer simulação. A heurística sugerida
pelo orquestrador (kill ~ t^β ⇒ ∫e^{−ct^{β+1}/(β+1)}) NÃO será aceita
sem derivação própria — a derivação decidirá (adianta-se: há um termo
de "crowding" que a heurística ignora; ver programa analítico).

## (1) Família paramétrica PRECISA de mecanismos (ensemble finito)

Base comum: π permutação uniforme de [n]. Um subconjunto R ⊆ [n] de
pontos "redirecionados" é sorteado pela regra do mecanismo;
f(i) = π(i) para i ∉ R e f(i) = D_i para i ∈ R, com destinos D_i
sorteados pela regra do mecanismo, independentes entre si dado (π, R).
Observável: φ^M(n,c) = E[#{i : ∃t≥1, f^t(i)=i}]/n; alvo
φ^M_∞(c) = lim_{n→∞} φ^M(n,c); expoente de cauda α tal que
φ^M_∞(c) ≍ c^{−α} (c→∞), com coeficiente quando derivável.

Mecanismos (todos bem definidos em n finito):

- **M-U (original; caso especial da família):** i ∈ R indep. w.p. c/n;
  D_i uniforme em [n].
- **M-CLUST(b), b=8 (reroteamento em blocos ao longo de π):** sementes
  S: cada i ∈ S indep. w.p. c/n; R = {π^j(i) : i ∈ S, 0 ≤ j ≤ b−1};
  D_i uniforme em [n], indep. para cada i ∈ R. (Nota: |R| ≈ b·c pontos,
  perturbação "b vezes maior" em massa que M-U.)
- **M-MIX(p), p=1/2 (mistura com auto-laço):** i ∈ R indep. w.p. c/n;
  D_i = i com prob. p, uniforme em [n] com prob. 1−p.
- **M-SELF (auto-laço puro; = M-MIX(1)):** i ∈ R indep. w.p. c/n;
  D_i = i. (Derivação + verificação já existente: massa cíclica de
  M-SELF = massa livre de reroteamento do u12, cujo valor
  (1−e^{−c})/c foi verificado no T4 da onda 2 e pelo adversário —
  não será re-simulado.)
- **M-PREV (antecessor):** i ∈ R indep. w.p. c/n; D_i = π^{−1}(i)
  (determinístico dado π).
- **M-INTRA (destino no próprio ciclo):** i ∈ R indep. w.p. c/n;
  D_i uniforme no ciclo de π contendo i, C_π(i). Implementação:
  D_i = π^{T_i}(i), T_i uniforme em {0,…,2³¹−1} (viés de uniformidade
  ≤ L/2³¹ ≤ n/2³¹ ≈ 1.5e−5 por destino em n = 2¹⁵ — declarado
  desprezível face às SEMs ~1e−2).

Classe abstrata (nível do processo-limite, NÃO um ensemble finito,
rotulada como tal): **M-q** — no processo de exploração da onda 2,
eventos de reroteamento a taxa c por unidade de massa percorrida;
evento no instante s mata a ciclicidade com prob. q(s), senão cria um
novo início de arco (destino em massa fresca). M-U é q(s)=s; M-SELF é
q≡1; fronteira **M-NOKILL** é q≡0 (sem realização intrínseca
conhecida; serve para demarcar o piso da classe).

## (2) Programa analítico pré-declarado (executar ANTES das simulações)

Registrar em `DERIVATIONS.md`, pela mesma rota PGFL da onda 2, com
rigor de rascunho de pesquisa e TODO passo heurístico rotulado:

1. **Fórmula-mestre para M-q:** φ_q(c) = ∫₀¹ e^{−c·H_q(t)} dt com
   H_q explícito (generalizando E[S(t)] = (1−t)e^{−ct²}).
2. **Lei do expoente:** de H_q, extrair α em função do comportamento
   q(s) ~ a·s^β (s→0⁺), incluindo o termo de crowding dos inícios de
   arco (que existe mesmo com q≡0); enunciar o TETO e o PISO de α
   sobre toda a classe M-q (0 ≤ q ≤ 1). É aqui que a heurística do
   orquestrador será confirmada ou corrigida.
3. **Por mecanismo:** (i) M-U: q=s + lema de intercambiabilidade
   (qualquer lei de destino simétrica em [n], independente de (π,R),
   coincide em lei com o uniforme); (ii) M-MIX(p): q = p+(1−p)s e
   forma fechada; (iii) M-SELF: q≡1 por exploração + rota finita-n
   independente; (iv) M-PREV: rota finita-n própria (2-ciclos) + rota
   por exploração; (v) M-CLUST(b): argumento de sombreamento
   (pontos de bloco não-iniciais são π-inalcançáveis) ⇒ predição no
   limite + alvo corrigido de n finito (correções O(bc/n) declaradas);
   (vi) M-INTRA: valor EXATO condicional a K=1 e primeira ordem a₁;
   análise de cauda HEURÍSTICA (círculo quenched) — expoente e
   coeficiente rotulados heurísticos.
4. **Bateria K=1 exata:** φ₁ = E[fração cíclica | exatamente 1
   reroteamento] para M-U, M-MIX(1/2), M-PREV/M-SELF, M-INTRA —
   valores racionais exatos, derivados por size-biasing (L ~ U(0,1)),
   independentes da fórmula-mestre.
5. **Alvos numéricos:** `predictions.py` → `predictions.json` com as
   quadraturas das fórmulas derivadas (dupla precisão) para toda a
   grade abaixo, ANTES de qualquer simulação.

## (3) Programa numérico pré-declarado

Simulador finito-n próprio, vetorizado (numpy): f construído
explicitamente; pontos cíclicos = imagem distinta de f^(2¹⁵) por
duplicação iterada (método validado pela verificação adversarial da
onda 2 em rota independente); n = 2¹⁵ = 32768 em TODAS as células.
Execução ÚNICA; bug descoberto ⇒ correção + reexecução COMPLETA com
novas sementes declaradas (nunca reexecução parcial).

- **B1 — curvas médias:** mecanismos [M-U, M-CLUST(8), M-MIX(1/2),
  M-PREV, M-INTRA] × c ∈ {0.5, 2, 10, 40, 160}; N = 3000
  realizações/célula; sementes: `SeedSequence(20260822)`, spawn de 25
  filhos na ordem (mecanismo na lista acima) × (c crescente).
  M-U é a FAIXA DE CONTROLE (predição já estabelecida; mede o viés
  finito-n do simulador por c). Células M-INTRA c ∈ {0.5, 2}:
  tabulação sem predição (declarado — não entram em critério).
- **B2 — condicional K=1:** exatamente 1 ponto redirecionado (posição
  uniforme), destino pela regra do mecanismo; mecanismos
  [M-U, M-MIX(1/2), M-PREV, M-INTRA]; N = 20000/célula;
  sementes: `SeedSequence(84206)`, spawn de 4 na ordem acima.
- **Runtime alvo:** ≤ 25 min total (foreground). Se estourar: reduzir
  N uniformemente à metade, DECLARANDO no log.
- SEM = desvio-padrão amostral/√N por célula; z = (φ_MC − alvo)/SEM.

## (4) Critérios de validação (pré-declarados)

- **C1 (curvas médias, mecanismos com forma derivada):** para
  M ∈ {M-U, M-CLUST(8) [alvo corrigido finito-n], M-MIX(1/2), M-PREV}:
  |z| < 4 por célula E χ²₅ com p ≥ 0.01 por mecanismo.
  **Regra da faixa de controle:** se a célula M-U de um dado c falhar
  |z| < 4, aquele c é declarado "limitado por viés finito-n em
  n = 32768" e as células dos demais mecanismos naquele c são
  reportadas mas excluídas de PASS/FAIL (regra simétrica, declarada
  antes de rodar). **Banda sistemática M-CLUST:** em c ∈ {40, 160}
  há correções conhecidas O(bc/n) (~4% em c=160) parcialmente
  canceladas; célula aceita se |z| < 4 OU desvio relativo < 2·bc/n
  (banda declarada).
- **C2 (K=1 exato):** |z| < 4 em cada um dos 4 alvos racionais.
- **C3 (expoentes de cauda):** α̂ = ln(φ̂(10)/φ̂(160))/ln 16 por
  mecanismo, σ_α̂ por propagação das SEMs. Aceite:
  |α̂ − α_alvo| < max(0.06, 3σ_α̂), com α_alvo = declive exato da
  forma derivada entre c=10 e 160 (M-U, M-CLUST, M-MIX, M-PREV — para
  os dois últimos isto testa α = 1 efetivo) e α_alvo = 1/2 para
  M-INTRA (predição de classe, de derivação heurística). O COEFICIENTE
  de cauda de M-INTRA é comparação apenas descritiva (heurístico,
  fator O(1) incerto — declarado).

## (5) Interpretação pré-declarada dos desfechos

- Todos os critérios passam ⇒ a tabela de classes de `DERIVATIONS.md`
  é promovida a resultado da frente com os rótulos
  DERIVADO/HEURÍSTICO/CONJECTURADO que cada linha carregar (a
  simulação não promove heurística a derivação).
- Falha em mecanismo com forma DERIVADA ⇒ a derivação daquele
  mecanismo é declarada refutada/incompleta (resultado negativo com
  peso igual; vai à tabela como tal).
- Falha só em M-INTRA (heurístico) ⇒ registra-se o expoente/curva
  MEDIDOS e a heurística é descartada como falha honesta.
- Em qualquer caso, a resposta às perguntas centrais 1–3 é redigida em
  `RESULTS_SUMMARY.md` citando o status de cada elo (derivado vs
  simulado vs conjecturado).

## Entregáveis

`METHODOLOGY_NOTE.md` (este), `DERIVATIONS.md`, `predictions.py` +
`predictions.json` (alvos pré-simulação), `ualpha_sim.py` +
`ualpha_results.json` + `ualpha_sim.log` (B1–B2 + critérios),
`RESULTS_SUMMARY.md` (PT, com a TABELA DE CLASSES:
mecanismo → φ_∞ → cauda → classe U_α → status).
