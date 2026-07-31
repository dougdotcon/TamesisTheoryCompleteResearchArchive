---
document_id: FSG2-RESULT-REVIEW
work_item_id: FOUND-SEMIGROUP-002
decision: A_FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
reviewed_commit: b4ce2551cd9f3588030fc7281d7f8c7aa624bac3
new_theorems: 0
lean_math_modules_modified: 0
---

# FOUND-SEMIGROUP-002 — Revisão de resultado

Revisão do que já está verificado. **Nenhum teorema novo. Nenhum módulo
matemático alterado.**

## Confirmação item a item

### FRR-001 — alcançabilidade

```text
CONFIRMADO
```

`reachable_refl` (testemunha `1`, via `one_smul`) e `reachable_trans`
(testemunha `n * m`, na ordem em que `m` age primeiro). Ambos valem para
**qualquer** monoide e qualquer ação — nenhuma finitude é exigida.

**Simetria não é afirmada em lugar algum.** `CE-001` a refuta.

### FRR-002 — órbita

```text
CONFIRMADO
```

`reachable_iff_mem_orbit : Reachable x y ↔ y ∈ MulAction.orbit M x`,
provado por `Iff.rfl`.

Auditoria de duplicidade: busca por `orbit` nos módulos da frente encontra
**apenas** `MulAction.orbit`. **Nenhuma segunda definição pública de
órbita existe.**

### FRR-003 — invariantes

```text
CONFIRMADO
```

- `IsInvariant.of_reachable` — preservação por alcançabilidade;
- `IsInvariant.under` — invariância sob qualquer elemento fixado;
- `IsInvariantUnder.pow` — propagação às potências.

**A recíproca de `IsInvariant.under` não é afirmada.** Verificado por
inspeção: não existe declaração cuja conclusão seja `IsInvariant` a partir
de `IsInvariantUnder`. A correção 5.1 do gate anterior está registrada em
`DEFINITIONS.md`, `KNOWN_RESULTS_MATRIX.md`, `RESULT_BOUNDARY.md` e no
docstring de `Invariants.lean`.

### FRR-004 — colisão limitada

```text
CONFIRMADO
```

```text
@exists_bounded_iterate_collision :
  ∀ {X : Type u_1} [inst : Fintype X] (f : X → X) (x : X),
    ∃ mu lam, mu < Fintype.card X ∧ 0 < lam ∧
      mu + lam ≤ Fintype.card X ∧ f^[mu + lam] x = f^[mu] x
```

Os quatro conjuntos exigidos estão na conclusão, e a única hipótese de
classe é `Fintype X`.

### FRR-005 — periodicidade eventual

```text
CONFIRMADO
```

`periodic_tail_of_collision : … → Function.IsPeriodicPt f lam (f^[mu] x)`.

O argumento é **`f^[mu] x`**, não `x`.

Sobre a palavra "período": `Function.IsPeriodicPt f n x` significa
`f^[n] x = x`, e **não** exige minimalidade. Nada nesta frente afirma
período mínimo. `Function.minimalPeriod` aparece **quatro vezes** nos
arquivos, todas em comentários explicando por que **não** é usado; zero
usos reais. `MulAction.period`: zero ocorrências.

### FRR-006 — propagação

```text
CONFIRMADO
```

```text
@collision_propagates :
  ∀ {X} (f : X → X) (x : X) {mu lam : ℕ},
    f^[mu + lam] x = f^[mu] x → ∀ (k : ℕ), f^[mu + k + lam] x = f^[mu + k] x
```

Aritmética dos índices, conferida linha a linha:

```text
mu + k + lam = k + (mu + lam)      (omega)
mu + k       = k + mu              (omega)

f^[k + (mu+lam)] x = f^[k] (f^[mu+lam] x)   Function.iterate_add_apply f k (mu+lam) x
f^[k + mu] x       = f^[k] (f^[mu] x)       Function.iterate_add_apply f k mu x
                                            depois h fecha por rfl
```

As duas aplicações de `iterate_add_apply` estão **explicitamente
instanciadas** — foi exatamente a falta disso que produziu a falha
corrigida no gate anterior.

### FRR-007 — ação por elemento

```text
CONFIRMADO
```

```text
@monoid_element_eventually_periodic :
  ∀ {M : Type u_1} {X : Type u_2} [inst : Monoid M] [inst_1 : Fintype X]
    [inst_2 : MulAction M X] (a : M) (x : X), …
```

Ausentes, como exigido: **`Fintype M`**, **`Group M`**, **`DecidableEq X`**.

## Caso `card X = 0`

```text
O teorema recebe x : X.

Portanto, no ponto de aplicacao, X eh habitado e card X > 0.
O caso card X = 0 nao produz contradicao escondida porque nao existe
termo x : X nesse caso — o teorema simplesmente nao pode ser invocado.
```

Consequência formal: a conclusão `mu < Fintype.card X` é satisfazível
sempre que o enunciado for aplicável. Se `card X = 0`, `mu < 0` seria
insatisfazível em `ℕ`, mas nenhuma instância do teorema existe ali, porque
`x : X` é premissa.

Auditoria da hipótese oculta: busca por `Nonempty` e `Inhabited` nos
módulos da frente devolve **zero ocorrências**. Nenhuma prova depende de
instância global desnecessária; a habitação vem do próprio argumento `x`.

## Casa dos pombos

```yaml
pigeonhole_uses_in_core: 1
bounded_collision_dependency: true
reproved_in_main_theorem: false
reproved_in_monoid_corollary: false
reproved_in_propagation: false
```

`Fintype.exists_ne_map_eq_of_card_lt` aparece **três vezes** textualmente:

```text
EventualPeriodicity.lean:54   USO REAL (unico)
EventualPeriodicity.lean:47   docstring
Audit.lean:51                 #check
```

Uso real: **um**. `exists_eventual_period`,
`monoid_element_eventually_periodic` e `collision_propagates` obtêm o
resultado por composição, não por reaplicação.

## Decisão

```text
A. FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED
```

Critérios verificados:

| Critério | Estado |
|---|---|
| teoremas compilam | `lake build` PASS |
| assinaturas mínimas | sem `DecidableEq X`, `Fintype M`, `Group M` |
| instâncias isoladas | 11, todas em namespaces de contraexemplo; **0 no núcleo** |
| contraexemplos válidos | `CE-001`–`CE-005` verificados |
| claim dentro do resultado | ver `FINAL_GAP_STATUS.md` e revisão da claim |
| limites científicos preservados | `RESULT_BOUNDARY.md`, `C3_BOUNDARY.md` vinculantes |
| sem dependência oculta de legado | imports auditados |
