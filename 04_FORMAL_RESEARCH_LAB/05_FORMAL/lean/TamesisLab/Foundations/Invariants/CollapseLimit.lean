import TamesisLab.Foundations.Invariants.Unreachability
import TamesisLab.Foundations.FiniteStateAbstraction.OrbitSeparation

set_option autoImplicit false

/-!
# FOUND-INVARIANT-UNREACHABILITY-001 — o limite do colapso

O resultado **negativo** da frente, e a razão de ela não ser reescrita de
nada.

A cadeia de dez frentes construiu abstração para **colapsar**: achar
recorrência no sistema abstrato e refleti-la no concreto, sob
`OrbitSeparating`. Esta frente construiu abstração para **separar**:
provar impossibilidade.

O teorema abaixo mede a distância exata entre os dois usos, e ela não é
zero.

```text
para abstracoes invariantes,
OrbitSeparating vale EXATAMENTE nos pontos fixos
```

Fora dos pontos fixos, um invariante nunca satisfaz a condição de
reflexão. Portanto **invariantes certificam impossibilidade e nunca
recorrência**: os dois usos da mesma máquina são incompatíveis.

A razão é simples e vale a pena ficar escrita. Com `stepA = id` a órbita
abstrata é constante, então a hipótese de `OrbitSeparating` é sempre
verdadeira, e a condição degenera em exigir que a órbita **concreta**
também seja constante.
-/

namespace TamesisLab.Foundations.Invariants

open TamesisLab.Foundations.FiniteStateAbstraction

variable {C A : Type*}

/-- **O limite do colapso.**

Para uma abstração invariante, a condição de reflexão da frente anterior
vale se e somente se o estado inicial é ponto fixo.

Uma hipótese, um ponto inicial. Nenhuma finitude, nenhuma decidibilidade,
nenhuma hipótese sobre a órbita. -/
theorem invariant_orbitSeparating_iff_fixedPoint {abstract : C → A} {stepC : C → C}
    (h : Invariant abstract stepC) (start : C) :
    OrbitSeparating abstract stepC start ↔ stepC start = start := by
  constructor
  · intro hsep
    have h1 := hsep 1 0 (by simpa using h start)
    simpa using h1
  · intro hfix i j _
    have hconst : ∀ k : Nat, (stepC^[k]) start = start := by
      intro k
      induction k with
      | zero => simp
      | succ n ih => rw [Function.iterate_succ_apply', ih, hfix]
    rw [hconst i, hconst j]

end TamesisLab.Foundations.Invariants
