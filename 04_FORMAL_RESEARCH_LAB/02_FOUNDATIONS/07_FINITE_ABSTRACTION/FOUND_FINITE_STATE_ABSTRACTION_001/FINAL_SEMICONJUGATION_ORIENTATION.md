---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-SEMICONJUGATION-ORIENTATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
---

# Orientação da semiconjugação — final

## Congelada

```text
abstract (stepC c) = stepA (abstract c)
```

## Evidência

Assinatura real, lida por `#check`:

```text
@Function.Semiconj :
  {α : Type u_1} → {β : Type u_2} →
  (α → β) → (α → α) → (β → β) → Prop
```

Desdobramento confirmado por `Iff.rfl`:

```lean
example {C A : Type} (abstract : C → A) (stepC : C → C) (stepA : A → A) :
    Function.Semiconj abstract stepC stepA
      ↔ ∀ c, abstract (stepC c) = stepA (abstract c) :=
  Iff.rfl
```

`Iff.rfl` é a evidência mais forte disponível: a equivalência vale por
definição, sem `simp`, sem `unfold`, sem conversão.

## Iteradas

```text
@Function.Semiconj.iterate_right :
  ∀ {α β} {f : α → β} {ga : α → α} {gb : β → β},
    Function.Semiconj f ga gb →
      ∀ (n : ℕ), Function.Semiconj f ga^[n] gb^[n]
```

Rota única para `iterate_commutes`. `iterate_left` **não** é usada.

## Inversão

Impossível por tipagem: `abstract : C → A` força `α := C`. A troca
silenciosa que `STOP-ABS-003` descreve não é expressável.

```text
STOP-ABS-003 disparada   NAO
```
