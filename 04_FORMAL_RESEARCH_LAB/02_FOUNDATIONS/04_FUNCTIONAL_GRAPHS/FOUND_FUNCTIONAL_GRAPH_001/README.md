# FOUND-FUNCTIONAL-GRAPH-001 — Grafos funcionais finitos

Especificação. **Nenhuma prova, nenhum arquivo Lean, nenhum `lake build`.**

## O objeto

```text
X : tipo finito
f : X → X
```

Cada estado tem exatamente uma transição seguinte. É a mesma estrutura da
Camada C de `FOUND-SEMIGROUP-002`; o que muda é a escala da pergunta — lá,
**uma trajetória**; aqui, a **estrutura global** do grafo.

## As três relações, que não podem ser confundidas

```text
IterReachable f x y      ∃ n, f^[n] x = y          alcancabilidade dirigida
MutuallyReachable f x y  vai e volta                mesmo CICLO
EventuallyMeets f x y    ∃ m n, f^[m] x = f^[n] y   mesmo COMPONENTE
```

**Componente funcional := classe de `EventuallyMeets`.** Não é
`MutuallyReachable` — ver `COMPONENT_NOTIONS.md` e o contraexemplo
decisivo `FFG-CE-004`:

```text
a → c
b → c
c → c
```

`a` e `b` estão no mesmo componente, e nenhum alcança o outro.

## Alvo

```text
CORE_UNIQUE_CYCLE_WITH_ENTRY_BOUND
```

Toda trajetória alcança um ponto periódico, e todos os pontos periódicos do
componente determinam **a mesma órbita periódica**.

O objeto único é `Function.periodicOrbit f p` — **não** o representante `p`.

## Artefatos

```text
STATUS.yaml                estado da frente
TARGET_RESULT.md           alvo e o significado exato de "unicidade"
DEFINITIONS.md             as tres relacoes, nomes e orientacao fixados
COMPONENT_NOTIONS.md       a escolha de componente — VINCULANTE
ASSUMPTIONS.md             hipoteses e negativas com contraexemplo
THEOREM_CANDIDATES.md      16 assinaturas, sem corpo de prova
THEOREM_DEPENDENCY_MAP.md  DAG da prova futura
LEAN_FEASIBILITY.md        DecidableEq, imports, custos, riscos
MATHLIB_API_AUDIT.md       23 itens lidos na fonte
COUNTEREXAMPLE_PLAN.md     FFG-CE-001..006
KNOWN_RESULTS_MATRIX.md    o que ja eh padrao
GAP_REGISTER.yaml          FFG-GAP-001..014
STOP_CONDITIONS.md         STOP-001..014
NOVELTY_BOUNDARY.md        fronteira de novidade — VINCULANTE
SPECIFICATION_DECISION.md  a decisao deste gate
```

## Relação com `FOUND-SEMIGROUP-002`

Reutilização de **API verificada**, não extensão de escopo. O
`extension_status` daquela frente permanece `NOT_AUTHORIZED`.

## Aviso vinculante

Decomposição de grafo funcional em ciclo mais trajetórias de entrada é a
"forma rho" da iteração finita — **material padrão**.
`mathematical_novelty: NONE`.
