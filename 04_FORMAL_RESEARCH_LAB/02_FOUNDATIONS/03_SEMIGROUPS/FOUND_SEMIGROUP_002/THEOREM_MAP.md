---
artifact_id: FOUND-SEMIGROUP-002
status: VERIFIED
lean_root: "05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/"
---

# FOUND-SEMIGROUP-002 — Mapa de teoremas

## Camada A — ação completa do monoide

| ID | Lean | Arquivo |
|---|---|---|
| — | `Reachable` (`def`) | `Reachability.lean` |
| `FSG2-REACH-001` | `reachable_refl` | `Reachability.lean` |
| `FSG2-REACH-002` | `reachable_trans` | `Reachability.lean` |
| `FSG2-REACH-003a` | `reachable_isRefl` | `Reachability.lean` |
| `FSG2-REACH-003b` | `reachable_isTrans` | `Reachability.lean` |
| `FSG2-ORBIT-001` | `reachable_iff_mem_orbit` | `Reachability.lean` |
| — | `IsInvariant`, `IsInvariantUnder` (`def`) | `Invariants.lean` |
| `FSG2-INV-001` | `IsInvariant.under` | `Invariants.lean` |
| `FSG2-INV-002` | `IsInvariant.of_reachable` | `Invariants.lean` |
| `FSG2-INV-003` | `IsInvariantUnder.pow` | `Invariants.lean` |

### Testemunhas

```text
reachable_refl        1 : M, via one_smul
reachable_trans       n * m, NESTA ordem (m age primeiro, convencao mul_smul)
reachable_iff_mem_orbit   Iff.rfl — a ponte eh DEFINICIONAL
```

### `Preorder` — decisão registrada

Nenhuma `instance : Preorder X` foi criada. A relação depende de `M`, que
não aparece no tipo `X`; duas ações distintas sobre o mesmo `X` produziriam
instâncias incompatíveis. Foram registradas apenas
`reachable_isRefl : Std.Refl _` e `reachable_isTrans : IsTrans X _`.

Nota de revisão: na Mathlib fixada `IsRefl` está **depreciada** em favor de
`Std.Refl` (com `α` implícito); `IsTrans` não está. Daí a assimetria entre
os dois enunciados. Ambos são `theorem`, nenhum é `instance`.

## Camada C — função sobre tipo finito (sem monoide)

| ID | Lean | Arquivo |
|---|---|---|
| — | `eventual_period_of_lt` (`private`) | `EventualPeriodicity.lean` |
| `FSG2-PER-001` | `exists_bounded_iterate_collision` | `EventualPeriodicity.lean` |
| `FSG2-PER-004` | `periodic_tail_of_collision` | `EventualPeriodicity.lean` |
| `FSG2-PER-003` | `collision_propagates` | `EventualPeriodicity.lean` |
| `FSG2-PER-002` | `exists_eventual_period` | `EventualPeriodicity.lean` |

### Origem dos índices repetidos

```text
g : Fin (Fintype.card X + 1) -> X,   g k = f^[k] x

Fintype.exists_ne_map_eq_of_card_lt g h
  com h : Fintype.card X < Fintype.card (Fin (card X + 1))

devolve  i != j  com  f^[i] x = f^[j] x
```

A casa dos pombos é aplicada **exatamente uma vez**, aqui.

### Tratamento de `i < j` e `j < i`

`lt_or_gt_of_ne hne` separa os dois casos; ambos são despachados pelo mesmo
auxiliar `eventual_period_of_lt`, com os argumentos trocados e a igualdade
simetrizada (`hEq.symm`) no segundo ramo. **Nenhuma duplicação de
argumento.**

### Limitantes

```text
i, j ∈ Fin (card X + 1)   ==>  i, j <= card X   (Nat.lt_succ_iff.mp _.isLt)
mu := i,  lam := j - i
mu = i < j <= card X       ==>  mu < card X
lam = j - i > 0            ==>  0 < lam
mu + lam = j <= card X     ==>  mu + lam <= card X
```

Os três limitantes saem por `omega` a partir de `i < j` e `j ≤ card X`.

### Ponto periódico na cauda

```lean
periodic_tail_of_collision : f^[mu + lam] x = f^[mu] x →
  Function.IsPeriodicPt f lam (f^[mu] x)
```

O argumento é `f^[mu] x`, **não** `x`. Prova: `show` desdobra
`IsPeriodicPt`, depois `Function.iterate_add_apply` e `Nat.add_comm`.
**`Function.minimalPeriod` não é usado em lugar algum.**

### Propagação

```lean
collision_propagates : f^[mu + lam] x = f^[mu] x → ∀ k, f^[mu+k+lam] x = f^[mu+k] x
```

Prova: reindexação por `omega` (`mu + k + lam = k + (mu + lam)`,
`mu + k = k + mu`), duas aplicações **explicitamente instanciadas** de
`Function.iterate_add_apply` e a hipótese. A casa dos pombos **não** é
reaplicada.

### Teorema principal

`exists_eventual_period` é **composição pura** dos três anteriores: um
`obtain` e um `exact` com a tripla. Nenhum passo analítico novo.

## Camada B — iteração de um elemento

| ID | Lean | Arquivo |
|---|---|---|
| `FSG2-ACT-001` | `monoid_element_eventually_periodic` | `MonoidIteration.lean` |
| `FSG2-ACT-002` | `monoid_element_eventual_period_propagates` | `MonoidIteration.lean` |

Derivados de `exists_bounded_iterate_collision` aplicado a
`fun y : X => a • y`, transportados por
`smul_iterate_apply : (a • ·)^[n] x = a ^ n • x`. **Sem reaplicar
pigeonhole.**

## Hipóteses efetivamente exigidas

Assinaturas impressas pelo build:

```text
@exists_eventual_period :
  ∀ {X : Type u_1} [inst : Fintype X] (f : X → X) (x : X), ...

@monoid_element_eventually_periodic :
  ∀ {M : Type u_1} {X : Type u_2} [inst : Monoid M] [inst_1 : Fintype X]
    [inst_2 : MulAction M X] (a : M) (x : X), ...
```

Ausentes, como planejado: **`DecidableEq X`**, **`Fintype M`**,
**`Group M`**. A hipótese `DecidableEq X` da assinatura originalmente
sugerida era de fato ociosa (`FSG2-GAP-004c` fechado).

## Contraexemplos

| ID | Lean | Refuta |
|---|---|---|
| `CE-001` | `Counterexamples.CE001.reachable_not_symmetric` | simetria de `Reachable` |
| `CE-002` | `Counterexamples.CE002.not_transitive` | transitividade da ação |
| `CE-003` | `Counterexamples.CE003.s0_not_periodic` | "eventual ⟹ periódico desde 0" |
| `CE-004` | `Counterexamples.CE004.not_faithful` | fidelidade |
| `CE-005` | `Counterexamples.CE005.invariant_does_not_separate_orbits` | invariante separa órbitas |

## Inventário

```text
inductives   6
defs        10
theorems    41
instances   11
structures   0
```
