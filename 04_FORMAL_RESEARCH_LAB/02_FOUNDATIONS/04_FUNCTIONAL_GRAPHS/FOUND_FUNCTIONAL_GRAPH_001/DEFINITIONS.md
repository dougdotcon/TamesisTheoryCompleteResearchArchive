# FOUND-FUNCTIONAL-GRAPH-001 — Definições

Assinaturas candidatas. **Nenhum corpo de prova. Nenhum arquivo Lean.**

## Dados centrais

```text
X : tipo finito
f : X → X
```

Cada estado tem exatamente uma transição seguinte. É a mesma estrutura da
Camada C de `FOUND-SEMIGROUP-002`; o que muda é a **escala da pergunta**:
lá, uma trajetória; aqui, a estrutura global.

---

## As três relações que não podem ser confundidas

### 1. Alcançabilidade dirigida

```lean
def IterReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ n : ℕ, f^[n] x = y
```

Leitura: *`y` ocorre na trajetória futura de `x`*.

```text
reflexiva      sim   (n = 0)
transitiva     sim   (via iterate_add_apply)
simetrica      NAO   (FFG-CE-002)
```

**Distinção de nível, herdada de `FOUND-SEMIGROUP-002`:** `IterReachable`
**não** é o `Reachable` da Camada A daquela frente, que quantifica sobre
todo um monoide. Se a formalização quiser conectar os dois, terá de
instanciar `Reachable` com o monoide livre de um gerador — e isso é
decisão de gate futuro, não dado desta especificação.

### 2. Alcançabilidade mútua

```lean
def MutuallyReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  IterReachable f x y ∧ IterReachable f y x
```

**Não é a definição de componente.** Ver `COMPONENT_NOTIONS.md`.

### Semântica precisa — corrigida na revisão

A redação anterior deste documento dizia que `MutuallyReachable`
"identifica estados do mesmo ciclo, e cada estado consigo próprio". Era
**imprecisa** como afirmação sobre todo o domínio. A formulação congelada
em `FINAL_DEFINITIONS.md` é:

```text
Em pontos periodicos, MutuallyReachable expressa pertencimento a mesma
trajetoria ciclica.

No conjunto total de estados:
- a classe de um ponto periodico p tem exatamente minimalPeriod f p
  elementos — os pontos do ciclo de p;
- cada ponto transitorio forma uma classe unitaria;
- portanto MutuallyReachable NAO representa a bacia funcional completa.
```

Refinamento acrescentado na revisão: "classe unitária" **não** distingue
transitório de ponto fixo — um ponto fixo é periódico e sua classe também é
unitária. O que distingue é a pertinência a `Function.periodicPts f`.

### 3. Encontro eventual — a relação central

```lean
def EventuallyMeets {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ m n : ℕ, f^[m] x = f^[n] y
```

Leitura: *as duas trajetórias eventualmente se encontram*.

## Decisão de nomenclatura

O gate ofereceu `SameFunctionalComponent` como nome semântico alternativo e
exigiu que **não** existam duas definições independentes com a mesma
semântica.

```yaml
decisao: uma unica definicao, chamada EventuallyMeets
rejeitado: "def SameFunctionalComponent := EventuallyMeets"
motivo_do_nome: >
  EventuallyMeets descreve o MECANISMO e casa com os nomes dos teoremas
  (eventuallyMeets_refl/symm/trans, periodicOrbit_eq_of_eventuallyMeets).
  "Mesmo componente funcional" eh a LEITURA da relacao, registrada aqui e
  em COMPONENT_NOTIONS.md, e nao um segundo objeto Lean.
rejeitado_tambem: >
  abbrev SameFunctionalComponent — mesmo com abbrev, dois nomes publicos
  para o mesmo predicado duplicam a superficie de API sem ganho.
```

---

## Conjunto componente

```lean
def componentSet {X : Type*} (f : X → X) (x : X) : Set X :=
  {y | EventuallyMeets f x y}
```

`Set X`, não `Finset X`: a finitude não é necessária para a definição, e
exigir `Fintype`/`DecidableEq` aqui seria hipótese ociosa — mesma política
que removeu `0 < c` em `COUNTING-LAW-BRIDGE` e `DecidableEq X` em
`FOUND-SEMIGROUP-002`.

**Nenhuma instância global de `Setoid` ou de equivalência será criada no
primeiro gate de formalização.** `EventuallyMeets` depende de `f`, que não
aparece no tipo `X`; uma instância seria o mesmo erro que
`FSG2-GAP-006` evitou com `Preorder`.

---

## Recorrência e transitoriedade

A fonte semântica é a Mathlib, e a definição já exige período positivo:

```lean
def periodicPts (f : α → α) : Set α := { x | ∃ n > 0, IsPeriodicPt f n x }
```

Aliases candidatos:

```lean
def IsRecurrent {X : Type*} (f : X → X) (x : X) : Prop :=
  x ∈ Function.periodicPts f

def IsTransient {X : Type*} (f : X → X) (x : X) : Prop :=
  ¬ IsRecurrent f x
```

### Decisão sobre os aliases — **REVERTIDA na revisão**

A decisão abaixo foi **retirada**. `IsRecurrent` **não** será publicado:
"recorrência" tem significados mais amplos em dinâmica. Os teoremas
públicos usam `x ∈ Function.periodicPts f` diretamente. Ver
`API_NAMING_DECISION.md` e `FINAL_DEFINITIONS.md`.

Registro histórico da decisão superada:

```yaml
decisao: CRIAR, com equivalencia definicional
justificativa: >
  `IsTransient` NAO existe na Mathlib e eh o conceito que a frente precisa
  nomear. Ter `IsRecurrent` ao lado dele mantem o par legivel e torna os
  enunciados simetricos. O custo eh uma linha, e a equivalencia eh `Iff.rfl`.
exigencia: >
  IsRecurrent f x ↔ x ∈ Function.periodicPts f  deve ser Iff.rfl,
  registrado como teorema de auditoria. Se deixar de ser, o alias virou
  uma segunda nocao e deve ser removido.
```

### Armadilha registrada

**Não** definir recorrência como `∃ n, f^[n] x = x`: com `n = 0` isso é
verdadeiro para todo estado, tornando a noção vazia. A definição da Mathlib
exige `n > 0`, e é por isso que ela é a fonte.

Herança direta de `FSG2-GAP-002b`: `Function.minimalPeriod` devolve `0`
fora de `periodicPts`, e por isso não serve como "período".

---

## Representação do ciclo

```lean
Function.periodicOrbit (f : α → α) (x : α) : Cycle α
```

`Cycle α := Quotient (IsRotated.setoid α)` — **igualdade a menos de
rotação**. É exatamente a propriedade que permite falar de "o ciclo" sem
escolher um vértice representante.

**Nenhuma estrutura própria de ciclo será criada.** `Function.periodicOrbit`
é suficiente; duplicá-la seria o erro que `FSG2-GAP-001` evitou ao
reutilizar `MulAction.orbit`.

---

## Orientação da igualdade de órbitas — regra fixada

O gate exigiu escolher uma orientação e mantê-la.

```text
REGRA: o primeiro argumento de EventuallyMeets vai para o lado ESQUERDO
       da igualdade de orbitas.
```

Consequências, ambas consistentes com a regra:

```lean
-- FFG-CYCLE-001: hipotese EventuallyMeets f p q
periodicOrbit f p = periodicOrbit f q

-- FFG-MAIN-001: a hipotese alimentada a CYCLE-001 eh EventuallyMeets f q p
periodicOrbit f q = periodicOrbit f p
```

No teorema principal, `q` é o ponto periódico **arbitrário** e `p` o
representante produzido pela existência; a conclusão lê-se "a órbita de
qualquer periódico do componente é a órbita de `p`".


---

# Estado após a revisão

Este documento é **histórico**. As definições vigentes estão em
`FINAL_DEFINITIONS.md` e as assinaturas em `FINAL_SIGNATURES.md`, ambas
congeladas no gate `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW`.

Correções aplicadas:

1. semântica de `MutuallyReachable` tornada precisa;
2. `IsRecurrent`/`IsTransient` **retirados**;
3. `componentSet` marcado `DEFERRED_API_ALIAS`;
4. testemunhas corrigidas para a forma natural de
   `Function.iterate_add_apply` (contagem externa à esquerda).
