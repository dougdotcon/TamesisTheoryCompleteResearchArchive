---
document_id: FCD-LEAN-API-AUDIT
revision_checked: 79d0395a1825a6264ad5d269e35e60537518955e
toolchain: leanprover/lean4:v4.33.0-rc1
probe: /tmp/CycleDetectionSpecificationProbe.lean (removido ao final)
---

# Auditoria da API Lean

Todas as assinaturas abaixo foram **impressas pelo próprio Lean** no
checkout fixado, via sonda temporária. Nenhum nome foi presumido.

## Construção de listas

```yaml
- concept: intervalo de naturais
  candidate_api: List.range
  source_file: Init/Data/List (core), reexportado via Mathlib.Data.List.Range
  exact_signature: "List.range : ℕ → List ℕ"
  revision_checked: v4.33.0-rc1
  classification: API_FOUND
  usable: true
  limitations: nenhuma
  fallback: List.range'

- concept: produto dependente de listas
  candidate_api: List.flatMap
  exact_signature: "@List.flatMap : {α : Type u_1} → {β : Type u_2} → (α → List β) → List α → List β"
  classification: API_FOUND
  usable: true
  limitations: "ordem dos argumentos: funcao primeiro, lista depois"
  fallback: List.bind (nome antigo)

- concept: imagem de lista
  candidate_api: List.map
  exact_signature: "@List.map : {α : Type u_1} → {β : Type u_2} → (α → β) → List α → List β"
  classification: API_FOUND
  usable: true

- concept: pertinencia a range
  candidate_api: List.mem_range
  exact_signature: "@List.mem_range : ∀ {m n : ℕ}, m ∈ List.range n ↔ m < n"
  classification: API_FOUND
  usable: true

- concept: pertinencia a flatMap
  candidate_api: List.mem_flatMap
  exact_signature: "@List.mem_flatMap : ∀ {α β} {f : α → List β} {b : β} {l : List α}, b ∈ List.flatMap f l ↔ ∃ a ∈ l, b ∈ f a"
  classification: API_FOUND
  usable: true
  limitations: "eh a peca central de mem_cycleCandidates_iff"

- concept: pertinencia a map
  candidate_api: List.mem_map
  exact_signature: "@List.mem_map : ∀ {α β} {b : β} {f : α → β} {l : List α}, b ∈ List.map f l ↔ ∃ a ∈ l, f a = b"
  classification: API_FOUND
  usable: true

- concept: comprimento de range
  candidate_api: List.length_range
  exact_signature: "@List.length_range : ∀ {n : ℕ}, (List.range n).length = n"
  classification: API_FOUND
  usable: true
  limitations: "so seria necessario para complexidade, que NAO esta autorizada"
```

## Busca em listas

```yaml
- concept: primeiro elemento que satisfaz um predicado
  candidate_api: List.find?
  exact_signature: "@List.find? : {α : Type u_1} → (α → Bool) → List α → Option α"
  classification: API_FOUND
  usable: true
  limitations: "o predicado eh Bool, nao Prop — por isso o decide"

- concept: soundness de find?
  candidate_api: List.find?_some
  exact_signature: "@List.find?_some : ∀ {α} {p : α → Bool} {a : α} {l : List α}, List.find? p l = some a → p a = true"
  classification: API_FOUND
  usable: true
  limitations: "peca central da soundness"

- concept: pertinencia do achado
  candidate_api: List.mem_of_find?_eq_some
  exact_signature: "@List.mem_of_find?_eq_some : ∀ {α} {p} {a} {l}, List.find? p l = some a → a ∈ l"
  classification: API_FOUND
  usable: true
  limitations: "nao usada no plano atual; disponivel"

- concept: caracterizacao de find? = some
  candidate_api: List.find?_eq_some_iff_append
  exact_signature: "@List.find?_eq_some_iff_append : ∀ {α} {b} {p} {xs}, List.find? p xs = some b ↔ p b = true ∧ ∃ as bs, xs = as ++ b :: bs ∧ ∀ a ∈ as, (!p a) = true"
  classification: API_FOUND
  usable: true
  limitations: >
    o nome sugerido pelo gate era List.find?_eq_some; o nome real nesta
    revisao eh List.find?_eq_some_iff_append. Da tambem a MINIMALIDADE
    posicional (nenhum anterior satisfaz p) — sera a chave de uma
    eventual prova de minimalidade, hoje NAO autorizada.

- concept: find? = none
  candidate_api: List.find?_eq_none
  exact_signature: "@List.find?_eq_none : ∀ {α} {p} {l}, List.find? p l = none ↔ ∀ x ∈ l, ¬p x = true"
  classification: API_FOUND
  usable: true
  limitations: "rota alternativa da completude, por contradicao"

- concept: isSome de find?
  candidate_api: List.find?_isSome
  exact_signature: "@List.find?_isSome : ∀ {α} {xs} {p}, (List.find? p xs).isSome = true ↔ ∃ x ∈ xs, p x = true"
  classification: API_FOUND
  usable: true
  limitations: "peca central da completude"

- concept: isSome como any
  candidate_api: List.isSome_find?
  exact_signature: "@List.isSome_find? : ∀ {α} {xs} {f}, (List.find? f xs).isSome = xs.any fun x => f x"
  classification: API_FOUND
  usable: true
  limitations: "variante booleana; nome quase identico ao anterior — atencao"

- concept: find? em cons
  candidate_api: List.find?_cons_of_pos / List.find?_cons_of_neg
  classification: API_FOUND
  usable: true
  limitations: "uteis para avaliar os casos de teste passo a passo"

- concept: indice do primeiro que satisfaz
  candidate_api: List.findIdx?
  exact_signature: "@List.findIdx? : {α : Type u_1} → (α → Bool) → List α → Option ℕ"
  classification: API_FOUND
  usable: false
  limitations: "devolve indice na lista, nao o certificado; NOT_NEEDED"

- concept: indice de um elemento
  candidate_api: List.idxOf?
  exact_signature: "@List.idxOf? : {α : Type u_1} → [BEq α] → α → List α → Option ℕ"
  classification: API_FOUND
  usable: false
  limitations: "exige BEq; NOT_NEEDED"

- concept: acesso indexado seguro
  candidate_api: List.get? / List.getElem?
  exact_signature: "—"
  classification: NOT_FOUND
  usable: false
  limitations: >
    nenhuma das duas existe como constante nesta revisao; o acesso
    indexado eh feito pela notacao l[i]? via a classe GetElem?.
  fallback: "notacao l[i]?; NOT_NEEDED no plano atual"
```

## Option

```yaml
- concept: presenca de valor
  candidate_api: Option.isSome
  exact_signature: "@Option.isSome : {α : Type u_1} → Option α → Bool"
  classification: API_FOUND
  usable: true

- concept: extracao com prova
  candidate_api: Option.get
  exact_signature: "@Option.get : {α : Type u_1} → (o : Option α) → o.isSome = true → α"
  classification: API_FOUND
  usable: true
  limitations: "a prova eh argumento Prop e eh apagada; base da totalizacao"

- concept: get de some
  candidate_api: Option.get_some
  exact_signature: "@Option.get_some : ∀ {α} (x : α) (h : (some x).isSome = true), (some x).get h = x"
  classification: API_FOUND
  usable: true

- concept: some do get
  candidate_api: Option.some_get
  exact_signature: "@Option.some_get : ∀ {α} {x : Option α} (h : x.isSome = true), some (x.get h) = x"
  classification: API_FOUND
  usable: true
  limitations: "peca para transportar a soundness ao wrapper total"

- concept: isSome como existencial
  candidate_api: Option.isSome_iff_exists
  exact_signature: "@Option.isSome_iff_exists : ∀ {α} {x : Option α}, x.isSome = true ↔ ∃ a, x = some a"
  classification: API_FOUND
  usable: true
  limitations: "fecha a completude"

- concept: none como negacao universal
  candidate_api: Option.eq_none_iff_forall_ne_some
  classification: API_FOUND
  usable: true
```

## Decidibilidade

```yaml
- concept: classe de decidibilidade
  candidate_api: Decidable
  exact_signature: "Decidable : Prop → Type"
  classification: API_FOUND
  usable: true

- concept: reflexao booleana
  candidate_api: decide
  exact_signature: "decide : (p : Prop) → [h : Decidable p] → Bool"
  classification: API_FOUND
  usable: true

- concept: ponte decide/Prop
  candidate_api: decide_eq_true_eq
  exact_signature: "@decide_eq_true_eq : ∀ {p : Prop} [inst : Decidable p], (decide p = true) = p"
  classification: API_FOUND
  usable: true
  limitations: "unica ponte Bool/Prop necessaria; evita duplicar o predicado"

- concept: decidibilidade da conjuncao
  candidate_api: instDecidableAnd
  exact_signature: "@instDecidableAnd : {p q : Prop} → [Decidable p] → [Decidable q] → Decidable (p ∧ q)"
  classification: API_FOUND
  usable: true

- concept: decidibilidade de < em Nat
  candidate_api: Nat.decLt
  exact_signature: "Nat.decLt : (n m : ℕ) → Decidable (n < m)"
  classification: API_FOUND
  usable: true

- concept: decidibilidade de = em Nat
  candidate_api: instDecidableEqNat / Nat.decEq
  classification: API_FOUND
  usable: true
  limitations: "nao usada diretamente; o que importa eh DecidableEq X"
```

## Finitude, iteração e periodicidade

```yaml
- concept: cardinalidade
  candidate_api: Fintype.card
  exact_signature: "Fintype.card : (α : Type u_1) → [Fintype α] → ℕ"
  classification: API_FOUND
  usable: true

- concept: iteracao de funcao
  candidate_api: Nat.iterate
  exact_signature: "@Nat.iterate : {α : Sort u_1} → (α → α) → ℕ → α → α"
  classification: API_FOUND
  usable: true
  limitations: >
    Function.iterate NAO existe como identificador nesta revisao. A
    notacao f^[n] resolve para Nat.iterate. O gate listou
    "Function.iterate"; o nome real eh Nat.iterate.

- concept: decomposicao da iteracao
  candidate_api: Function.iterate_add_apply
  exact_signature: "@Function.iterate_add_apply : ∀ {α} (f : α → α) (m n : ℕ) (x : α), f^[m + n] x = f^[m] (f^[n] x)"
  classification: API_FOUND
  usable: true
  limitations: "contagem externa a ESQUERDA — orientacao ja auditada na frente anterior"

- concept: ponto periodico
  candidate_api: Function.IsPeriodicPt
  exact_signature: "@Function.IsPeriodicPt : {α : Type u_1} → (α → α) → ℕ → α → Prop"
  classification: API_FOUND
  usable: true

- concept: conjunto de pontos periodicos
  candidate_api: Function.periodicPts
  exact_signature: "@Function.periodicPts : {α : Type u_1} → (α → α) → Set α"
  classification: API_FOUND
  usable: true

- concept: introducao em periodicPts
  candidate_api: Function.mk_mem_periodicPts
  exact_signature: "@Function.mk_mem_periodicPts : ∀ {α} {f} {x} {n}, 0 < n → Function.IsPeriodicPt f n x → x ∈ Function.periodicPts f"
  classification: API_FOUND
  usable: true
  limitations: "consome exatamente o 0 < period do certificado"

- concept: periodo minimo
  candidate_api: Function.minimalPeriod
  exact_signature: "@Function.minimalPeriod : {α : Type u_1} → (α → α) → α → ℕ"
  classification: API_FOUND
  usable: false
  limitations: "NOT_NEEDED — minimalidade NAO esta autorizada; o campo period NAO eh minimalPeriod"
```

## APIs do próprio laboratório

```yaml
- concept: colisao limitada
  candidate_api: FiniteDynamics.exists_bounded_iterate_collision
  exact_signature: >
    ∀ {X} [Fintype X] (f : X → X) (x : X), ∃ mu lam,
      mu < Fintype.card X ∧ 0 < lam ∧ mu + lam ≤ Fintype.card X ∧
      f^[mu + lam] x = f^[mu] x
  classification: API_FOUND
  usable: true
  limitations: "coincide TERMO A TERMO com CycleWitness.Valid"

- concept: cauda periodica
  candidate_api: FiniteDynamics.periodic_tail_of_collision
  exact_signature: >
    ∀ {X} (f : X → X) (x : X) {mu lam}, f^[mu + lam] x = f^[mu] x →
      Function.IsPeriodicPt f lam (f^[mu] x)
  classification: API_FOUND
  usable: true
  limitations: "sem Fintype, sem DecidableEq"

- concept: propagacao da colisao
  candidate_api: FiniteDynamics.collision_propagates
  exact_signature: >
    ∀ {X} (f : X → X) (x : X) {mu lam}, f^[mu + lam] x = f^[mu] x →
      ∀ k, f^[mu + k + lam] x = f^[mu + k] x
  classification: API_FOUND
  usable: true
  limitations: "assinatura IDENTICA a de CycleWitness.propagates"

- concept: periodicidade eventual
  candidate_api: FiniteDynamics.exists_eventual_period
  classification: API_FOUND
  usable: false
  limitations: "composicao das tres anteriores; o detector usa as pecas, nao o pacote"

- concept: entrada limitada no ciclo
  candidate_api: FunctionalGraphs.exists_cyclePoint_reachable_with_bound
  classification: API_FOUND
  usable: false
  limitations: "NOT_NEEDED — o certificado ja da mu diretamente"

- concept: orbita unica do componente
  candidate_api: FunctionalGraphs.exists_component_cycle_with_entry_bound
  classification: API_FOUND
  usable: true
  limitations: "usada na ponte OPCIONAL com o componente funcional"

- concept: igualdade de orbita por encontro
  candidate_api: FunctionalGraphs.periodicOrbit_eq_of_eventuallyMeets
  classification: API_FOUND
  usable: true
  limitations: "exige AMBOS os pontos periodicos — restricao vinculante herdada"
```

## Resumo

```text
API_FOUND        31
NOT_FOUND         1   (List.get? / List.getElem?)
NAME_UNCERTAIN    0
NOT_NEEDED        5   (findIdx?, idxOf?, minimalPeriod,
                       exists_eventual_period, exists_cyclePoint_...)
```

Dois nomes do gate divergem do checkout e foram corrigidos:
`List.find?_eq_some` → `List.find?_eq_some_iff_append`;
`Function.iterate` → `Nat.iterate`.
