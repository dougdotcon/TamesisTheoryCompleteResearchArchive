---
document_id: FFG-FINAL-DEFINITIONS
status: FROZEN
gate: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW
---

# FOUND-FUNCTIONAL-GRAPH-001 — Definições congeladas

Estas são as definições autorizadas para a formalização. Qualquer desvio
exige gate próprio.

## As três relações

```lean
def IterReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ n : ℕ, f^[n] x = y

def MutuallyReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  IterReachable f x y ∧ IterReachable f y x

def EventuallyMeets {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ m n : ℕ, f^[m] x = f^[n] y
```

Nenhuma exige `Fintype X`, `DecidableEq X`, `Nonempty X` ou `Inhabited X`.

## `SameFunctionalComponent` — não criado

Nem como `def`, nem como `abbrev`. `EventuallyMeets` é o único nome
público; "mesmo componente funcional" é a sua **leitura**.

## `componentSet` — adiado

```yaml
componentSet:
  status: DEFERRED_API_ALIAS
```

Nenhum teorema `CORE` congelado o utiliza. Criar uma definição pública sem
uso contradiria o princípio já aplicado nesta frente. Se a formalização
descobrir um teorema público que o exija, ele volta com justificativa.

## Recorrência — sem alias público

`IsRecurrent` **não** será publicado. Ver `API_NAMING_DECISION.md`.

Os teoremas públicos usam diretamente:

```lean
x ∈ Function.periodicPts f
x ∉ Function.periodicPts f
```

---

## Semântica precisa de `MutuallyReachable` — correção obrigatória

A redação anterior — *"`MutuallyReachable` identifica o ciclo, não o
componente"* — era imprecisa como afirmação sobre todo o domínio. A
formulação correta:

```text
Em pontos periodicos, MutuallyReachable expressa pertencimento a mesma
trajetoria ciclica.

No conjunto total de estados:

- os pontos de cada ciclo formam uma classe cujo tamanho eh o comprimento
  do ciclo;
- cada ponto transitorio forma uma classe unitaria;
- portanto MutuallyReachable NAO representa a bacia funcional completa nem
  o componente definido por encontro eventual.
```

### Refinamento adicional

A frase "classe não trivial" só é exata para ciclos de comprimento maior
que um. Um **ponto fixo** é periódico e sua classe também é unitária. O
enunciado preciso é:

```text
a classe de MutuallyReachable de um ponto periodico p tem exatamente
minimalPeriod f p elementos — os pontos do ciclo de p.

Ela eh unitaria exatamente quando p eh ponto fixo.
```

Logo "classe unitária" **não** distingue transitório de ponto fixo; o que
distingue é a pertinência a `Function.periodicPts f`.

### Argumento de que todo ponto transitório é isolado

```text
Suponha x ≠ y, IterReachable f x y e IterReachable f y x.
Existem n1 com f^[n1] x = y, e n2 com f^[n2] y = x.
Entao f^[n2 + n1] x = f^[n2] (f^[n1] x) = f^[n2] y = x.
Se n1 = n2 = 0 entao y = x, contra a hipotese; logo n2 + n1 > 0.
Portanto x ∈ Function.periodicPts f.

Contrapositivo: se x eh transitorio, nenhum y ≠ x eh mutuamente
alcancavel com x. A classe de x eh {x}.
```

Note a ordem `n2 + n1`: a contagem **externa** vem primeiro em
`Function.iterate_add_apply`. Ver `FINAL_SIGNATURES.md`.

### Lema candidato

```lean
theorem mutuallyReachable_of_periodicOrbit_eq
```

Classificado **`OPTIONAL`**. Não é parte do teorema principal e não é
dependência de nada no `CORE`.

---

## Fontes da Mathlib congeladas

```lean
Function.periodicPts (f : α → α) : Set α
Function.mem_periodicPts : x ∈ periodicPts f ↔ ∃ n > 0, IsPeriodicPt f n x
Function.mk_mem_periodicPts (hn : 0 < n) (hx : IsPeriodicPt f n x) : x ∈ periodicPts f
Function.periodicOrbit (f : α → α) (x : α) : Cycle α
Function.periodicOrbit_apply_iterate_eq (hx) (n) :
  periodicOrbit f (f^[n] x) = periodicOrbit f x
Function.mem_periodicOrbit_iff (hx) : y ∈ periodicOrbit f x ↔ ∃ n, f^[n] x = y
Function.self_mem_periodicOrbit (hx) : x ∈ periodicOrbit f x
Function.periodicOrbit_eq_nil_iff_not_periodic_pt :
  periodicOrbit f x = Cycle.nil ↔ x ∉ periodicPts f
Function.iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)
```

Todas confirmadas por probe descartável em `/tmp`, exit 0, removido.

### `IsPeriodicPt` isolada não serve

`Function.IsPeriodicPt f 0 x` é `f^[0] x = x`, isto é `x = x` — **sempre
verdadeiro**. Usá-la sozinha para definir pertinência ao ciclo tornaria
todo estado cíclico. `periodicPts` exige `∃ n > 0` e é por isso a fonte.

### Não computabilidade de `periodicOrbit`

`periodicOrbit` está em `noncomputable section`. Consequência:

```text
NAO impede provas proposicionais.
IMPEDE tratar igualdade de orbitas como decisao por `decide` sem
infraestrutura adicional.
```

Afeta apenas `FFG-CE-005`, que usará `periodicOrbit_apply_iterate_eq`.
