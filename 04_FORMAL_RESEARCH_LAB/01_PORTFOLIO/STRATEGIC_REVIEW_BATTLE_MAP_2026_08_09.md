---
document_id: STRATEGIC-REVIEW-BATTLE-MAP-2026-08-09
reviewed_at: 2026-08-09
requested_by: "principal do laboratório (direção de pesquisa explícita, ver DECISION_LEDGER DEC-065)"
conclusion: NS_FOUNDATIONS_SELECTED_AS_FRONT_OF_HIGHEST_CONCENTRATION
---

# Revisão estratégica — mapa de batalha das seis linhas de pesquisa

## Por que este documento existe

O usuário pediu, nestes termos: uma revisão do que falta construir em
cada linha, identificar a mais frágil, e construir o que falta para
"atacar" — parando apenas quando prontos para o ataque. Este documento
responde a isso, mas com uma tradução obrigatória para a linguagem deste
laboratório: aqui **não existe "atacar" um Problema do Milênio**. Isso é
proibido em todo `stop_condition` registrado, em `AGENTS.md`, e em cada
gate desta sessão. A tradução honesta de "preparar o ataque" é: **manter
o maior volume possível de infraestrutura formal correta, verificada e
sem sorry, no ponto de maior alavancagem, e nomear com precisão cirúrgica
a lacuna matemática que continua genuinamente aberta** — para que, se e
quando a lacuna real puder ser fechada (por este laboratório ou por
qualquer outra pessoa), o terreno já esteja preparado. "Fragilidade" aqui
significa **onde a fronteira entre o que já está provado e o que falta é
mais nítida e mais bem instrumentada** — não "onde é mais fácil resolver
o problema de milênio". Nenhuma das seis linhas está perto disso, e este
documento não finge o contrário.

## O tabuleiro, linha por linha

### 1. Riemann (`RH-NOGO-001`) — travada, não reativável por este gate

`FROZEN_PARTIAL_RESULT` desde 2026-07-31. `RH_NOGO_REACTIVATION_CRITERIA.md`
lista cinco condições (`REACT-001` a `REACT-005`): biblioteca Lean para
operadores autoadjuntos não limitados com resolvente compacto,
formalização reutilizável da lei GLOBAL de Weyl, formalização de
Riemann–von Mangoldt, colaborador comprometido com a camada concreta, ou
prioridade estratégica registrada. **Nenhuma ocorreu.** O próprio
documento nomeia explicitamente o padrão que estaria acontecendo agora se
eu reabrisse esta frente por conta própria: *"um gate autônomo decidir
que agora vale a pena"* — a primeira entrada da lista do que **não**
conta como reativação. Esta linha fica travada. Não é a mais frágil; é a
mais protegida contra reabertura prematura, de propósito.

### 2. Navier-Stokes (`NS-PRESSURE-001`, cadeia `FOUND-*`) — infraestrutura mais profunda do laboratório

O que já está **verificado, com `lake build` exit 0, zero sorry**:

```text
FOUND-SOBOLEV-SPACE-001              H^s como tipo normado completo
FOUND-LERAY-PROJECTOR-001            projetor de Leray em L², limitado/idempotente
FOUND-LERAY-PROJECTOR-SOBOLEV-001    o mesmo projetor levantado para H^s
FOUND-LERAY-PROJECTOR-SOBOLEV-ORTHOGONAL-001
                                     autoadjunção/projeção ortogonal em H^s
FOUND-FOURIER-MULTIPLIER-L2-001      cálculo de multiplicador de Fourier em L²,
                                     SEM exigir HasTemperateGrowth (extensão real
                                     sobre o Mathlib, não colagem)
Helmholtz.lean                       decomposição P + Q completa, ambos
                                     autoadjuntos, idempotentes, ortogonais,
                                     soma = identidade
PressureHessianAlgebra.lean          tr(AΩ)=0 e identidades correlatas
                                     (álgebra linear finita, VERIFICADO)
```

O que está genuinamente aberto (`NS-GAP-001`/`004`, "Lemma 3.1" do
documento legado): a parte anisotrópica do Hessiano de pressão é uma
integral singular tipo Biot–Savart/Riesz sem fórmula local fechada;
nenhuma estimativa quantitativa dela foi encontrada ou produzida nesta
sessão. A avaliação registrada (`GAP_REGISTER.yaml`, `stop_condition`) é
que essa lacuna tem a mesma estrutura de dificuldade de todo critério de
regularidade condicional já publicado e nunca verificado a priori
(Constantin–Fefferman 1993, tipo Prodi–Serrin, Evan Miller 2020) — **não
uma prova formal de equivalência, mas motivo suficiente para não tentar
forçar uma prova do Lemma 3.1 nesta sessão nem em nenhuma sessão
autônoma**. `NS-GAP-003` (a forma nua do Alignment Gap) já foi **refutada
por contraexemplo explícito e verificado computacionalmente** nesta
sessão (equação de Euler restrita, Vieillefosse 1982) — um resultado
formal real, mas negativo: elimina uma simplificação ingênua, não abre
caminho para a Millennium.

**Esta é a linha de maior concentração de força.** Nenhuma outra linha
tem seis módulos Lean verificados encadeados. É "frágil" no sentido
estratégico correto: a fronteira entre infraestrutura provada e a lacuna
real é a mais nítida de todo o portfólio, e o próximo tijolo de
infraestrutura (ver abaixo) está a um passo de distância, sem tocar
`NS-GAP-001`.

### 3. P vs NP (`PVSNP-PHYS-001`) — auditoria concluída, sem infraestrutura nova identificada

A auditoria desta sessão (`03_MILLENNIUM/03_P_VS_NP/`) delimitou escopo
com precisão bibliográfica; os 4 gaps registrados (`PNP-GAP-001` a
`004`) são majoritariamente conceituais/bibliográficos, não peças de
Lean formalizáveis com o material disponível. Nenhum item novo e
executável foi encontrado.

### 4. Yang-Mills (`YM-LIMIT-001`) — sete gaps, o mais recente é vigilância bibliográfica

`YM-GAP-007` (achado na própria revisão adversarial desta sessão): duas
preprints de 2025/2026 alegam prova construtiva completa de existência e
mass gap para SU(3)/SU(N) 4D. Uma foi retirada pelo arXiv; a outra segue
publicada, não verificada por pares. Este laboratório **não verifica nem
refuta** essas alegações — não é uma lacuna de infraestrutura Lean, é
monitoramento bibliográfico externo. Os demais gaps (`YM-GAP-001` a
`006`) envolvem construção de QFT que excede o que Mathlib oferece hoje.

### 5. Hodge (`HODGE-CDK-001`) — quatro gaps, infraestrutura ausente do Mathlib

Os gaps exigem infraestrutura de geometria algébrica/complexa que o
Mathlib não tem hoje (formas harmônicas, cohomologia de Dolbeault em
profundidade). Não é uma lacuna que este laboratório possa fechar com
engenharia de Lean nesta janela de tempo.

### 6. BSD (`BSD-HYP-MATRIX-001`) — seis gaps, majoritariamente bibliográficos/rastreamento de hipóteses

Auditoria já delimitou quais resultados dependem de quais hipóteses
(Birch–Swinnerton-Dyer completo, GRH, etc.). `EllipticHeight.lean` já
cobre a função altura ingênua e o paralelogramo condicional — extensão
adicional exigiria formalização de curvas elípticas além do que o
Mathlib oferece prontamente (alturas canônicas, L-funções).

## Os quatro gaps já nomeados como elegíveis (path 3 da revisão anterior)

`PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md` nomeou explicitamente:
`SC-GAP-002`, `LP-GAP-004` (fechado nesta sessão), `ENC-GAP-020`,
`RT-GAP-017` (caso geral), `YM-GAP-007`. Avaliação de cada um dos que
restam:

```text
SC-GAP-002   Enumeração ℕ→ℝ monótona + HilbertBasis de autovetores.
             Deliberadamente deixada aberta em FOUND-SPECTRAL-COUNTING-001:
             "~500+ linhas e NÃO é necessária para N(λ)". Nenhum consumidor
             novo surgiu nesta sessão que justifique os ~500 linhas agora.
             Não selecionada.

ENC-GAP-020  Invariância do witness concreto sob recodificação.
             Rejeitada não uma, mas QUATRO vezes em revisões de portfólio
             anteriores (AFTER-FINITE-STATE-ABSTRACTION, AFTER-BISIMULATION,
             AFTER-FRONTMATTER-SCAN, AFTER-CERTIFIED-ENCODING) pelo mesmo
             motivo: acoplamento à ordem de enumeração do detector.
             Não selecionada -- reabrir sem argumento novo repetiria uma
             decisão já tomada quatro vezes.

RT-GAP-017   Correção de uma abstração de sistema real (caso geral).
             O próprio registro diz "permanece aberto, e provavelmente
             permanecerá" -- é uma obrigação que pertence a quem produz o
             sistema real sendo abstraído, não a este laboratório.
             Não selecionada -- não é uma lacuna de formalização Lean.

YM-GAP-007   Vigilância bibliográfica de duas preprints externas.
             Não é infraestrutura para construir; é observação passiva.
             Não selecionada como alvo de construção (mantida como
             vigilância).
```

Nenhum dos quatro gaps pré-nomeados é hoje o alvo certo. Isso é
consistente com `PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md` — a fila
estava genuinamente esgotada para execução autônoma.

## O que abre a próxima frente, então

A diretriz estratégica explícita do usuário nesta sessão — "revise as
linhas, identifique a mais frágil, construa o que falta" — é, ela mesma,
a **via 2** que `PORTFOLIO_REVIEW_QUEUE_EXHAUSTED_2026_08_09.md` deixou
aberta: *"o principal do laboratório registrar uma nova entrada em
RESEARCH_QUEUE.yaml, com target_statement, expected_product e
stop_condition próprios — uma decisão de direção de pesquisa, não uma
decisão de execução"*. Não é um gate autônomo decidindo por conta própria
que "agora vale a pena" (o padrão proibido) — é o principal do
laboratório dando a direção; a execução que segue apenas instancia essa
direção com o rigor de sempre.

## Decisão

**Linha selecionada: Navier–Stokes / Foundations**, por concentração de
infraestrutura já provada e proximidade estrutural ao próximo tijolo
necessário. **Não** por proximidade à resolução do problema de milênio —
`NS-GAP-001` continua tão distante quanto estava.

**Próximo artefato**: o semigrupo do calor `e^{tΔ}` como multiplicador de
Fourier limitado em L² (símbolo real, contração, autoadjunto — via a
extensão já verificada `fourierMulL2`/`inner_fourierMulL2_symm`, que não
exige `HasTemperateGrowth`), composto com o projetor de Leray já
totalmente caracterizado, dando o operador de Stokes `P·e^{tΔ}` — o
bloco de construção padrão que qualquer formalização futura da fórmula
de Duhamel/solução branda de Navier–Stokes vai precisar. **A lei de
semigrupo `S(t+r) = S(t)∘S(r)` e a continuidade forte em `t` NÃO serão
demonstradas nesta frente** — exigem álgebra adicional sobre produtos de
elementos de `Lp ∞` não verificada nesta sessão; ficam registradas como
gap deliberadamente aberto, no mesmo padrão já usado para `SC-GAP-002` e
`LP-GAP-005` originalmente.

## O que este documento NÃO afirma

```text
que Navier-Stokes ficou mais tratável ou mais perto de solução
que o Lemma 3.1 / NS-GAP-001 / NS-GAP-004 tem caminho de prova
que "atacar" significa qualquer coisa além de construir infraestrutura
  formal correta e nomear com precisão o que continua em aberto
que RH-NOGO-001 foi reativada
que qualquer uma das quatro lacunas pré-nomeadas (SC-GAP-002, ENC-GAP-020,
  RT-GAP-017, YM-GAP-007) foi fechada por este documento
```
