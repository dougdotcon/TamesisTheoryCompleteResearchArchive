---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-SEMICONJUGATION-ORIENTATION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Orientação da semiconjugação

## Assinatura real, medida

```text
@Function.Semiconj :
  {α : Type u_1} → {β : Type u_2} →
  (α → β) → (α → α) → (β → β) → Prop
```

Lida em `lake env lean`, não citada de memória.

```text
primeiro argumento    a funcao,        α → β
segundo argumento     o passo em α
terceiro argumento    o passo em β
```

## A instanciação da frente

```text
α := C     o sistema concreto
β := A     o sistema abstrato

Function.Semiconj abstract stepC stepA
```

Desdobrada:

```text
∀ c : C,  abstract (stepC c) = stepA (abstract c)
```

Confirmado por `Iff.rfl` no probe: a definição desdobra exatamente nessa
igualdade, sem `simp` e sem conversão.

## Por que essa direção, e não a inversa

```text
o sistema concreto e o que EXECUTA
o sistema abstrato e o que se OBSERVA

um passo concreto, observado, e um passo abstrato
```

`Function.Semiconj abstract stepA stepC` afirmaria que `abstract`
transporta o passo **abstrato** para o **concreto** — o tipo nem
elabora, pois `abstract : C → A` obriga `α := C`. A troca silenciosa é
impossível por tipagem, e mesmo assim é auditada aqui porque
`STOP-ABS-003` a nomeia.

## A API de iteradas

```text
@Function.Semiconj.iterate_right :
  ∀ {α β} {f : α → β} {ga : α → α} {gb : β → β},
    Function.Semiconj f ga gb →
      ∀ (n : ℕ), Function.Semiconj f ga^[n] gb^[n]
```

`iterate_right` itera o **par de passos**, preservando `f`. É
exatamente o que a correspondência de iteradas pede; `iterate_left`
resolveria outro problema.

## Verificação

```text
orientacao congelada        abstract (stepC c) = stepA (abstract c)
confirmada por              Iff.rfl
inversao possivel           NAO, barrada por tipagem
STOP-ABS-003 disparada      NAO
```
