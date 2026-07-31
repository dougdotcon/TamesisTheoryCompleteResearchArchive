import TamesisLab.Foundations.FunctionalGraphs.ComponentCycle
import Mathlib.Data.Finset.Insert
import Mathlib.Data.Fintype.Defs

set_option autoImplicit false

/-!
# FOUND-FUNCTIONAL-GRAPH-001 — Contraexemplos

Seis modelos finitos, cada um refutando uma afirmação distinta. Cada um em
namespace próprio; nenhuma instância no namespace principal.

## Restrição de método

`Function.periodicOrbit` é **noncomputável**. Portanto `decide` **não** se
aplica a igualdade de órbitas — `FFG-CE-003` e `FFG-CE-005` usam
`periodicOrbit_apply_iterate_eq`. Nenhum `native_decide` em lugar algum.
-/

namespace TamesisLab.Foundations.FunctionalGraphs.Counterexamples

/-! ## FFG-CE-001 — dois ciclos globais distintos -/
namespace CE001

inductive St where
  | a
  | b
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a, .b}
  complete := fun x => by cases x <;> decide

/-- Dois pontos fixos independentes. -/
def f : St → St
  | .a => .a
  | .b => .b

theorem iterate_a (n : ℕ) : f^[n] St.a = St.a := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih]; rfl

theorem iterate_b (n : ℕ) : f^[n] St.b = St.b := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih]; rfl

theorem a_periodic : St.a ∈ Function.periodicPts f := ⟨1, by omega, rfl⟩

theorem b_periodic : St.b ∈ Function.periodicPts f := ⟨1, by omega, rfl⟩

/-- CE-001 — não existe ciclo global único: `a` e `b` são periódicos e
não pertencem ao mesmo componente. -/
theorem not_meets : ¬ EventuallyMeets f St.a St.b := by
  rintro ⟨m, n, h⟩
  rw [iterate_a, iterate_b] at h
  exact absurd h (by decide)

end CE001

/-! ## FFG-CE-002 — cauda antes do ciclo -/
namespace CE002

inductive St where
  | a
  | b
  | c
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a, .b, .c}
  complete := fun x => by cases x <;> decide

/-- `a → b → c → c`. -/
def f : St → St
  | .a => .b
  | .b => .c
  | .c => .c

theorem c_periodic : St.c ∈ Function.periodicPts f := ⟨1, by omega, rfl⟩

theorem reach_a_c : IterReachable f St.a St.c := ⟨2, rfl⟩

theorem meets_a_c : EventuallyMeets f St.a St.c := reach_a_c.eventuallyMeets

theorem iterate_ge_two (n : ℕ) (hn : 2 ≤ n) : f^[n] St.a = St.c := by
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hn
  clear hn
  induction m with
  | zero => decide
  | succ m ih =>
      rw [show 2 + (m + 1) = (2 + m) + 1 from by omega,
        Function.iterate_succ_apply', ih]
      rfl

/-- CE-002 — o estado inicial é transitório: não é periódico para período
positivo algum. -/
theorem a_not_periodic : St.a ∉ Function.periodicPts f := by
  rintro ⟨n, hn, h⟩
  have h' : f^[n] St.a = St.a := h
  rcases Nat.lt_or_ge n 2 with hlt | hge
  · have hn1 : n = 1 := by omega
    subst hn1
    exact absurd h' (by decide)
  · rw [iterate_ge_two n hge] at h'
    exact absurd h' (by decide)

end CE002

/-! ## FFG-CE-003 — ciclo de comprimento maior que um -/
namespace CE003

inductive St where
  | a
  | b
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a, .b}
  complete := fun x => by cases x <;> decide

/-- `a ↔ b`. -/
def f : St → St
  | .a => .b
  | .b => .a

theorem a_periodic : St.a ∈ Function.periodicPts f := ⟨2, by omega, rfl⟩

theorem b_periodic : St.b ∈ Function.periodicPts f := ⟨2, by omega, rfl⟩

theorem a_ne_b : St.a ≠ St.b := by decide

/-- CE-003 — o ciclo **não** é um ponto fixo. -/
theorem not_fixed : f St.a ≠ St.a := by decide

/-- As duas órbitas coincidem, provado por `periodicOrbit_apply_iterate_eq`
e **não** por `decide`, que não se aplica a objeto noncomputável. -/
theorem orbit_eq :
    Function.periodicOrbit f St.b = Function.periodicOrbit f St.a :=
  Function.periodicOrbit_apply_iterate_eq a_periodic 1

end CE003

/-! ## FFG-CE-004 — mesmo componente sem alcance mútuo

O contraexemplo **decisivo**: refuta `MutuallyReachable` como definição de
componente. -/
namespace CE004

inductive St where
  | a
  | b
  | c
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a, .b, .c}
  complete := fun x => by cases x <;> decide

/-- `a → c ← b`, com `c → c`. -/
def f : St → St
  | .a => .c
  | .b => .c
  | .c => .c

/-- Ambas as trajetórias caem em `c` num passo. -/
theorem meets_a_b : EventuallyMeets f St.a St.b := ⟨1, 1, rfl⟩

theorem iterate_a_ge_one (n : ℕ) (hn : 1 ≤ n) : f^[n] St.a = St.c := by
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hn
  clear hn
  induction m with
  | zero => decide
  | succ m ih =>
      rw [show 1 + (m + 1) = (1 + m) + 1 from by omega,
        Function.iterate_succ_apply', ih]
      rfl

theorem iterate_b_ge_one (n : ℕ) (hn : 1 ≤ n) : f^[n] St.b = St.c := by
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hn
  clear hn
  induction m with
  | zero => decide
  | succ m ih =>
      rw [show 1 + (m + 1) = (1 + m) + 1 from by omega,
        Function.iterate_succ_apply', ih]
      rfl

theorem not_reach_a_b : ¬ IterReachable f St.a St.b := by
  rintro ⟨n, hn⟩
  rcases Nat.eq_zero_or_pos n with rfl | hpos
  · exact absurd hn (by decide)
  · rw [iterate_a_ge_one n hpos] at hn
    exact absurd hn (by decide)

theorem not_reach_b_a : ¬ IterReachable f St.b St.a := by
  rintro ⟨n, hn⟩
  rcases Nat.eq_zero_or_pos n with rfl | hpos
  · exact absurd hn (by decide)
  · rw [iterate_b_ge_one n hpos] at hn
    exact absurd hn (by decide)

/-- CE-004 — `EventuallyMeets` **não** implica `MutuallyReachable`. -/
theorem not_mutually_reachable : ¬ MutuallyReachable f St.a St.b := by
  rintro ⟨h, -⟩
  exact not_reach_a_b h

end CE004

/-! ## FFG-CE-005 — vários pontos cíclicos, uma única órbita

Reutiliza o ciclo de dois estados de `CE-003`, com pergunta diferente. -/
namespace CE005

/-- CE-005 — dois pontos periódicos **distintos** com a **mesma** órbita.
Refuta "um único ponto periódico por componente" e confirma que o objeto
único é a órbita. -/
theorem distinct_points_same_orbit :
    CE003.St.a ≠ CE003.St.b ∧
      CE003.St.a ∈ Function.periodicPts CE003.f ∧
      CE003.St.b ∈ Function.periodicPts CE003.f ∧
      Function.periodicOrbit CE003.f CE003.St.b =
        Function.periodicOrbit CE003.f CE003.St.a :=
  ⟨CE003.a_ne_b, CE003.a_periodic, CE003.b_periodic, CE003.orbit_eq⟩

end CE005

/-! ## FFG-CE-006 — mesmo período mínimo, componentes distintos -/
namespace CE006

inductive St where
  | a0
  | a1
  | b0
  | b1
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a0, .a1, .b0, .b1}
  complete := fun x => by cases x <;> decide

/-- Dois 2-ciclos disjuntos: `a0 ↔ a1` e `b0 ↔ b1`. -/
def f : St → St
  | .a0 => .a1
  | .a1 => .a0
  | .b0 => .b1
  | .b1 => .b0

theorem a0_isPeriodic : Function.IsPeriodicPt f 2 St.a0 := rfl

theorem b0_isPeriodic : Function.IsPeriodicPt f 2 St.b0 := rfl

theorem a0_periodic : St.a0 ∈ Function.periodicPts f :=
  Function.mk_mem_periodicPts (by omega) a0_isPeriodic

theorem b0_periodic : St.b0 ∈ Function.periodicPts f :=
  Function.mk_mem_periodicPts (by omega) b0_isPeriodic

/-- Auxiliar: o período mínimo de um 2-ciclo é exatamente 2. -/
private theorem minimalPeriod_eq_two {s : St}
    (hper : Function.IsPeriodicPt f 2 s) (hmem : s ∈ Function.periodicPts f)
    (hfix : ¬ Function.IsFixedPt f s) :
    Function.minimalPeriod f s = 2 := by
  have hdvd : Function.minimalPeriod f s ∣ 2 := hper.minimalPeriod_dvd
  have hpos : 0 < Function.minimalPeriod f s :=
    Function.minimalPeriod_pos_of_mem_periodicPts hmem
  have hle : Function.minimalPeriod f s ≤ 2 := Nat.le_of_dvd (by omega) hdvd
  have hne : Function.minimalPeriod f s ≠ 1 := by
    intro h
    exact hfix (Function.minimalPeriod_eq_one_iff_isFixedPt.mp h)
  omega

theorem a0_minimalPeriod : Function.minimalPeriod f St.a0 = 2 :=
  minimalPeriod_eq_two a0_isPeriodic a0_periodic (by decide)

theorem b0_minimalPeriod : Function.minimalPeriod f St.b0 = 2 :=
  minimalPeriod_eq_two b0_isPeriodic b0_periodic (by decide)

theorem iterate_a0 (n : ℕ) : f^[n] St.a0 = St.a0 ∨ f^[n] St.a0 = St.a1 := by
  induction n with
  | zero => left; rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      rcases ih with h | h <;> rw [h] <;> decide

theorem iterate_b0 (n : ℕ) : f^[n] St.b0 = St.b0 ∨ f^[n] St.b0 = St.b1 := by
  induction n with
  | zero => left; rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      rcases ih with h | h <;> rw [h] <;> decide

/-- CE-006 — mesmo período mínimo, componentes distintos. -/
theorem same_period_different_component :
    Function.minimalPeriod f St.a0 = Function.minimalPeriod f St.b0 ∧
      ¬ EventuallyMeets f St.a0 St.b0 := by
  refine ⟨by rw [a0_minimalPeriod, b0_minimalPeriod], ?_⟩
  rintro ⟨m, n, h⟩
  rcases iterate_a0 m with ha | ha <;> rcases iterate_b0 n with hb | hb <;>
    rw [ha, hb] at h <;> exact absurd h (by decide)

end CE006

end TamesisLab.Foundations.FunctionalGraphs.Counterexamples
