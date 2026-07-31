import Mathlib.Logic.Function.Iterate
import Mathlib.Order.Defs.Unbundled

set_option autoImplicit false

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — Relações

Três relações sobre um grafo funcional `f : X → X`, deliberadamente
distintas:

```text
IterReachable f x y      ∃ n, f^[n] x = y          alcance dirigido
MutuallyReachable f x y  vai e volta                mesmo CICLO
EventuallyMeets f x y    ∃ m n, f^[m] x = f^[n] y   mesmo COMPONENTE
```

**Nenhuma exige finitude.** `Fintype X` só aparece em `ComponentCycle.lean`.

## Aviso de homonímia

`IterReachable` **não** é o `Reachable` de `FOUND-SEMIGROUP-002`, que
quantifica sobre um monoide, nem `SimpleGraph.Reachable`, que é não
dirigido. O prefixo `Iter` é deliberado.

## Orientação de `Function.iterate_add_apply`

```lean
Function.iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)
```

A contagem **externa** é `m` e fica à **esquerda** da soma. Todas as
testemunhas abaixo estão nessa forma natural; escrevê-las invertidas
exigiria `Nat.add_comm` para casar com `rw`.
-/

namespace TamesisLab.Foundations.FunctionalGraphs

/-- `y` ocorre na trajetória futura de `x`. -/
def IterReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ n : ℕ, f^[n] x = y

/-- Alcance nas duas direções.

Em grafo funcional, isto expressa pertinência à mesma trajetória cíclica —
**não** é a definição de componente. Ver `FFG-CE-004`. -/
def MutuallyReachable {X : Type*} (f : X → X) (x y : X) : Prop :=
  IterReachable f x y ∧ IterReachable f y x

/-- As trajetórias de `x` e `y` eventualmente se encontram.

**Esta é a relação de componente funcional.** Justificativa: numa função
determinística, depois que duas trajetórias atingem o mesmo estado, suas
continuações são idênticas. -/
def EventuallyMeets {X : Type*} (f : X → X) (x y : X) : Prop :=
  ∃ m n : ℕ, f^[m] x = f^[n] y

/-! ## Alcance dirigido -/

/-- FFG-REACH-001 — reflexividade, testemunha `0`. -/
theorem iterReachable_refl {X : Type*} (f : X → X) (x : X) :
    IterReachable f x x :=
  ⟨0, rfl⟩

/-- FFG-REACH-002 — transitividade.

Testemunha **`b + a`**, e não `a + b`: a contagem externa de
`Function.iterate_add_apply` vem à esquerda. -/
theorem iterReachable_trans {X : Type*} {f : X → X} {x y z : X}
    (hxy : IterReachable f x y) (hyz : IterReachable f y z) :
    IterReachable f x z := by
  obtain ⟨a, ha⟩ := hxy
  obtain ⟨b, hb⟩ := hyz
  refine ⟨b + a, ?_⟩
  rw [Function.iterate_add_apply, ha, hb]

/-- FFG-MEET-004 — alcance implica encontro, testemunhas `(n, 0)`. -/
theorem IterReachable.eventuallyMeets {X : Type*} {f : X → X} {x y : X}
    (h : IterReachable f x y) : EventuallyMeets f x y := by
  obtain ⟨n, hn⟩ := h
  exact ⟨n, 0, hn⟩

/-! ## Encontro eventual -/

/-- FFG-MEET-001 — reflexividade, testemunhas `(0, 0)`. -/
theorem eventuallyMeets_refl {X : Type*} (f : X → X) (x : X) :
    EventuallyMeets f x x :=
  ⟨0, 0, rfl⟩

/-- FFG-MEET-002 — simetria, por troca das testemunhas. -/
theorem eventuallyMeets_symm {X : Type*} {f : X → X} {x y : X}
    (h : EventuallyMeets f x y) : EventuallyMeets f y x := by
  obtain ⟨m, n, hmn⟩ := h
  exact ⟨n, m, hmn.symm⟩

/-- FFG-MEET-003 — transitividade.

Alinha as duas iteradas da trajetória intermediária `y`, comparando `ny` e
`my`. Os dois casos são explícitos; **nenhuma finitude é usada**. -/
theorem eventuallyMeets_trans {X : Type*} {f : X → X} {x y z : X}
    (hxy : EventuallyMeets f x y) (hyz : EventuallyMeets f y z) :
    EventuallyMeets f x z := by
  obtain ⟨mx, ny, hxy'⟩ := hxy
  obtain ⟨my, nz, hyz'⟩ := hyz
  rcases Nat.le_total ny my with h | h
  · -- ny ≤ my: avançar o lado de x em d = my - ny
    refine ⟨(my - ny) + mx, nz, ?_⟩
    have hd : (my - ny) + ny = my := by omega
    calc f^[(my - ny) + mx] x
        = f^[my - ny] (f^[mx] x) := Function.iterate_add_apply f _ _ _
      _ = f^[my - ny] (f^[ny] y) := by rw [hxy']
      _ = f^[(my - ny) + ny] y := (Function.iterate_add_apply f _ _ _).symm
      _ = f^[my] y := by rw [hd]
      _ = f^[nz] z := hyz'
  · -- my ≤ ny: avançar o lado de z em d = ny - my
    refine ⟨mx, (ny - my) + nz, ?_⟩
    have hd : (ny - my) + my = ny := by omega
    calc f^[mx] x
        = f^[ny] y := hxy'
      _ = f^[(ny - my) + my] y := by rw [hd]
      _ = f^[ny - my] (f^[my] y) := Function.iterate_add_apply f _ _ _
      _ = f^[ny - my] (f^[nz] z) := by rw [hyz']
      _ = f^[(ny - my) + nz] z := (Function.iterate_add_apply f _ _ _).symm

/-! ## Empacotamento relacional — **sem instâncias**

Nenhuma `instance : Setoid X` e nenhuma instância de equivalência. A
relação depende de `f`, que não aparece no tipo `X`; uma instância global
seria o mesmo erro que `FSG2-GAP-006` evitou com `Preorder`. -/

/-- Reflexividade empacotada. `Std.Refl` e não `IsRefl`: esta última está
depreciada na revisão fixada. -/
theorem eventuallyMeets_isRefl {X : Type*} (f : X → X) :
    Std.Refl (EventuallyMeets f) :=
  ⟨eventuallyMeets_refl f⟩

/-- Simetria empacotada. `Std.Symm` e não `Symmetric`: esta última também
está depreciada nesta revisão. -/
theorem eventuallyMeets_isSymm {X : Type*} (f : X → X) :
    Std.Symm (EventuallyMeets f) :=
  ⟨fun _ _ h => eventuallyMeets_symm h⟩

/-- Transitividade empacotada. -/
theorem eventuallyMeets_isTrans {X : Type*} (f : X → X) :
    IsTrans X (EventuallyMeets f) :=
  ⟨fun _ _ _ => eventuallyMeets_trans⟩

end TamesisLab.Foundations.FunctionalGraphs
