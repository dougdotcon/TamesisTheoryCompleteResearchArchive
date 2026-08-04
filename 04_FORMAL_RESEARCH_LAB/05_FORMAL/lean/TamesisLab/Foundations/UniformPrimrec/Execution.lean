import TamesisLab.Foundations.ComputabilityBridge
import Mathlib.Computability.Primrec.List

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — execucao

`run?_eq_iterate` e a declaracao central da frente: ela reescreve uma
recursao com `Option` como uma **iterada**, e e o que libera
`Primrec.nat_iterate`.

O obstaculo do nivel uniforme nunca foi computabilidade — era tipo
dependente. `run?` ja e `Nat -> Nat -> Option Nat`, sem `Fin`, e por isso
esta camada sai barata.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

theorem primrec_next_toList : Primrec fun t : RawTransitionTable => t.next.toList :=
  Primrec.of_equiv (e := rawTableEquiv)

theorem primrec_size : Primrec fun t : RawTransitionTable => t.next.size :=
  (Primrec.list_length.comp primrec_next_toList).of_eq (fun t => by simp)

theorem primrec_witness_pair :
    Primrec fun w : CycleWitness => (w.baseIndex, w.period) :=
  Primrec.of_equiv (e := cycleWitnessEquiv)

theorem primrec_baseIndex : Primrec CycleWitness.baseIndex :=
  Primrec.fst.comp primrec_witness_pair

theorem primrec_period : Primrec CycleWitness.period :=
  Primrec.snd.comp primrec_witness_pair

theorem primrec_mk : Primrec₂ fun b p : Nat => (⟨b, p⟩ : CycleWitness) := by
  have h : Primrec fun q : Nat × Nat => cycleWitnessEquiv.symm q :=
    Primrec.of_equiv_symm (e := cycleWitnessEquiv)
  exact h.of_eq (fun _ => rfl)


theorem primrec_step? : Primrec₂ RawTransitionTable.step? := by
  have h : Primrec₂ fun (t : RawTransitionTable) (s : Nat) => t.next.toList[s]? :=
    Primrec.list_getElem?.comp₂ (primrec_next_toList.comp Primrec.fst) Primrec.snd
  exact h.of_eq (fun t s => by simp [RawTransitionTable.step?])

theorem iterate_bind_none (f : Nat → Option Nat) (k : Nat) :
    (fun o : Option Nat => o.bind f)^[k] none = none := by
  induction k with
  | zero => rfl
  | succ k ih => rw [Function.iterate_succ_apply]; simpa using ih

theorem run?_eq_iterate (t : RawTransitionTable) (k : Nat) (state : Nat) :
    t.run? k state = (fun o : Option Nat => o.bind t.step?)^[k] (some state) := by
  induction k generalizing state with
  | zero => rfl
  | succ k ih =>
      rw [Function.iterate_succ_apply]
      show t.run? (k + 1) state = _
      cases hs : t.step? state with
      | none => simp [RawTransitionTable.run?, hs, iterate_bind_none]
      | some s' => simp [RawTransitionTable.run?, hs, ih s']

/-- `run?` de um argumento arbitrario. -/
theorem primrec_run?_gen {α : Type*} [Primcodable α]
    {ft : α → RawTransitionTable} {fk : α → Nat} {fs : α → Nat}
    (ht : Primrec ft) (hk : Primrec fk) (hs : Primrec fs) :
    Primrec fun a => (ft a).run? (fk a) (fs a) := by
  have hiter : Primrec fun a =>
      (fun o : Option Nat => o.bind (ft a).step?)^[fk a] (some (fs a)) := by
    refine Primrec.nat_iterate hk (Primrec.option_some.comp hs) ?_
    exact Primrec.option_bind Primrec.snd
      (primrec_step?.comp₂ (ht.comp (Primrec.fst.comp Primrec.fst)) Primrec.snd)
  exact hiter.of_eq (fun a => (run?_eq_iterate (ft a) (fk a) (fs a)).symm)


end TamesisLab.Foundations.UniformPrimrec
