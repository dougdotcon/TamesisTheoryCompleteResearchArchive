import TamesisLab.Foundations.FiniteDynamics.Reachability
import TamesisLab.Foundations.FiniteDynamics.Invariants
import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity
import Mathlib.Data.Finset.Insert
import Mathlib.Data.Fintype.Defs

set_option autoImplicit false

/-!
# FOUND-SEMIGROUP-002 — Contraexemplos finitos

Cinco modelos que impedem que propriedades do modelo `C3` de
`FOUND-SEMIGROUP-001` sejam promovidas a leis gerais.

Ordem seguida em cada modelo, herdada de `FOUND-SEMIGROUP-001`: definir a
operação → provar as leis → só então instanciar. Nenhuma instância é usada
para provar retroativamente as próprias leis.

Cada modelo vive em seu próprio namespace; não há duas instâncias globais
conflitantes para a mesma combinação de tipos.

## Correção obrigatória em CE-001

`Reachable` é definida pela **ação completa** do monoide. Portanto o grafo
de uma função isolada `f : X → X` **não** refuta a simetria de `Reachable`
— refuta apenas a alcançabilidade por iterações daquele gerador. `CE-001`
usa, por isso, uma **ação genuína de monoide**, com as leis verificadas.
-/

namespace TamesisLab.Foundations.FiniteDynamics.Counterexamples

/-! ## CE-001 — alcançabilidade não é simétrica

Monoide de duas transformações — identidade e colapso — agindo sobre dois
estados. Ação **completa**, não apenas uma função. -/
namespace CE001

inductive St where
  | zero
  | one
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.zero, .one}
  complete := fun x => by cases x <;> decide

inductive Tr where
  | idT
  | collapse
  deriving DecidableEq, Repr

instance : Fintype Tr where
  elems := {.idT, .collapse}
  complete := fun x => by cases x <;> decide

/-- Ação: `idT` fixa tudo, `collapse` manda tudo para `one`. -/
def act : Tr → St → St
  | .idT, s => s
  | .collapse, _ => .one

/-- Composição: `comp a b` aplica `b` primeiro (convenção de `mul_smul`). -/
def comp : Tr → Tr → Tr
  | .idT, t => t
  | .collapse, _ => .collapse

theorem comp_assoc (a b c : Tr) : comp (comp a b) c = comp a (comp b c) := by
  revert a b c; decide

theorem idT_comp (a : Tr) : comp .idT a = a := rfl

theorem comp_idT (a : Tr) : comp a .idT = a := by cases a <;> rfl

theorem act_comp (a b : Tr) (s : St) : act (comp a b) s = act a (act b s) := by
  revert a b s; decide

instance : Monoid Tr where
  mul := comp
  mul_assoc := comp_assoc
  one := .idT
  one_mul := idT_comp
  mul_one := comp_idT

instance : MulAction Tr St where
  smul := act
  one_smul := fun _ => rfl
  mul_smul := act_comp

/-- Toda transformação fixa o estado `one`. -/
theorem act_one (m : Tr) : act m St.one = St.one := by cases m <;> rfl

/-- `zero` alcança `one`, pela transformação `collapse`. -/
theorem reachable_zero_one : Reachable (M := Tr) St.zero St.one :=
  ⟨.collapse, rfl⟩

/-- Mas `one` **não** alcança `zero`: nenhuma transformação do monoide o faz. -/
theorem not_reachable_one_zero : ¬ Reachable (M := Tr) St.one St.zero := by
  rintro ⟨m, hm⟩
  have h : St.one = St.zero := by
    rw [← act_one m]
    exact hm
  exact absurd h (by decide)

/-- CE-001 — a alcançabilidade **não** é simétrica; logo não é relação de
equivalência. -/
theorem reachable_not_symmetric :
    Reachable (M := Tr) St.zero St.one ∧ ¬ Reachable (M := Tr) St.one St.zero :=
  ⟨reachable_zero_one, not_reachable_one_zero⟩

end CE001

/-! ## CE-002 — uma ação finita não precisa ser transitiva

Monoide trivial agindo pela identidade sobre dois estados: duas órbitas
disjuntas. -/
namespace CE002

inductive St where
  | a
  | b
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.a, .b}
  complete := fun x => by cases x <;> decide

inductive Tr where
  | idT
  deriving DecidableEq, Repr

instance : Fintype Tr where
  elems := {.idT}
  complete := fun x => by cases x; decide

def act : Tr → St → St
  | .idT, s => s

def comp : Tr → Tr → Tr
  | .idT, .idT => .idT

theorem comp_assoc (x y z : Tr) : comp (comp x y) z = comp x (comp y z) := by
  revert x y z; decide

theorem idT_comp (x : Tr) : comp .idT x = x := by cases x; rfl

theorem comp_idT (x : Tr) : comp x .idT = x := by cases x; rfl

theorem act_comp (x y : Tr) (s : St) : act (comp x y) s = act x (act y s) := by
  revert x y s; decide

instance : Monoid Tr where
  mul := comp
  mul_assoc := comp_assoc
  one := .idT
  one_mul := idT_comp
  mul_one := comp_idT

instance : MulAction Tr St where
  smul := act
  one_smul := fun _ => rfl
  mul_smul := act_comp

theorem act_a (m : Tr) : act m St.a = St.a := by cases m; rfl

/-- CE-002 — existem estados mutuamente inalcançáveis: a ação não é
transitiva. -/
theorem not_reachable_a_b : ¬ Reachable (M := Tr) St.a St.b := by
  rintro ⟨m, hm⟩
  have h : St.a = St.b := by
    rw [← act_a m]
    exact hm
  exact absurd h (by decide)

theorem not_transitive : ∃ x y : St, ¬ Reachable (M := Tr) x y :=
  ⟨St.a, St.b, not_reachable_a_b⟩

end CE002

/-! ## CE-003 — cauda antes do ciclo

Camada C pura: uma função sobre três estados, sem monoide. O estado inicial
é eventualmente periódico mas **não** é periódico — é por isso que
`Function.minimalPeriod` não pode ser usado como período eventual. -/
namespace CE003

inductive St where
  | s0
  | s1
  | s2
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.s0, .s1, .s2}
  complete := fun x => by cases x <;> decide

/-- `0 ↦ 1 ↦ 2 ↦ 2`: cauda de comprimento 2 antes do ponto fixo. -/
def f : St → St
  | .s0 => .s1
  | .s1 => .s2
  | .s2 => .s2

theorem not_fixed : f St.s0 ≠ St.s0 := by decide

theorem iterate_one : f^[1] St.s0 = St.s1 := by decide

theorem iterate_two : f^[2] St.s0 = St.s2 := by decide

/-- A trajetória é eventualmente fixa: `μ = 2`, `λ = 1`. -/
theorem eventually_fixed : f^[2 + 1] St.s0 = f^[2] St.s0 := by decide

/-- A partir do índice 2 a trajetória é constante igual a `s2`. -/
theorem iterate_ge_two (n : ℕ) (hn : 2 ≤ n) : f^[n] St.s0 = St.s2 := by
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hn
  clear hn
  induction m with
  | zero => decide
  | succ m ih =>
      rw [show 2 + (m + 1) = (2 + m) + 1 from by omega,
        Function.iterate_succ_apply', ih]
      rfl

/-- CE-003 — o estado inicial **não** é periódico para período algum
positivo, apesar de a trajetória ser eventualmente periódica.

Consequência: `Function.minimalPeriod f St.s0 = 0`, e usá-lo como "período
eventual" contradiria `0 < λ`. -/
theorem s0_not_periodic : ¬ ∃ n : ℕ, 0 < n ∧ f^[n] St.s0 = St.s0 := by
  rintro ⟨n, hn, h⟩
  rcases Nat.lt_or_ge n 2 with hlt | hge
  · have : n = 1 := by omega
    subst this
    exact absurd h (by decide)
  · rw [iterate_ge_two n hge] at h
    exact absurd h (by decide)

/-- O ponto periódico é `f^[2] St.s0`, **não** `St.s0`. -/
theorem periodic_point_is_tail : Function.IsPeriodicPt f 1 (f^[2] St.s0) :=
  periodic_tail_of_collision f St.s0 eventually_fixed

end CE003

/-! ## CE-004 — uma ação finita não precisa ser fiel

O monoide de `CE-001` agindo sobre um único estado: dois elementos
distintos induzem a **mesma** função. -/
namespace CE004

inductive St where
  | pt
  deriving DecidableEq, Repr

instance : Fintype St where
  elems := {.pt}
  complete := fun x => by cases x; decide

def act : CE001.Tr → St → St := fun _ _ => .pt

theorem act_comp (a b : CE001.Tr) (s : St) : act (a * b) s = act a (act b s) := by
  cases s; rfl

instance : MulAction CE001.Tr St where
  smul := act
  one_smul := fun s => by cases s; rfl
  mul_smul := act_comp

/-- CE-004 — a ação não é fiel: `idT ≠ collapse`, mas ambas agem
identicamente sobre `St`. -/
theorem not_faithful :
    ∃ a b : CE001.Tr, a ≠ b ∧ ∀ s : St, a • s = b • s :=
  ⟨.idT, .collapse, by decide, fun s => by cases s; rfl⟩

end CE004

/-! ## CE-005 — um invariante não separa órbitas

Reutiliza o modelo de `CE-002`: duas órbitas disjuntas e um invariante
constante. -/
namespace CE005

/-- Invariante constante. -/
def I : CE002.St → PUnit := fun _ => PUnit.unit

theorem I_isInvariant : IsInvariant (M := CE002.Tr) I :=
  fun _ _ => rfl

/-- CE-005 — `I` é invariante e assume o mesmo valor em duas órbitas
distintas. Logo a recíproca de `IsInvariant.of_reachable` é **falsa**: um
invariante refuta alcançabilidade, nunca a demonstra. -/
theorem invariant_does_not_separate_orbits :
    IsInvariant (M := CE002.Tr) I ∧
      I CE002.St.a = I CE002.St.b ∧
      ¬ Reachable (M := CE002.Tr) CE002.St.a CE002.St.b :=
  ⟨I_isInvariant, rfl, CE002.not_reachable_a_b⟩

end CE005

end TamesisLab.Foundations.FiniteDynamics.Counterexamples
