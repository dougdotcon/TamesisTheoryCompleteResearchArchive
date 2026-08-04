import TamesisLab.Foundations.UniformPrimrec.Execution

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — candidatos

O Mathlib oferece `Primrec` de `foldr`, nao de `flatMap`. A ponte de uma
linha entre os dois esta aqui.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

theorem flatMap_eq_foldr {α β : Type*} (f : α → List β) (l : List α) :
    l.flatMap f = l.foldr (fun a acc => f a ++ acc) [] := by
  induction l with
  | nil => rfl
  | cons a l ih => rw [List.flatMap_cons, ih, List.foldr_cons]

theorem primrec_cycleCandidates : Primrec cycleCandidates := by
  have hinner : Primrec fun q : (Nat × (Nat × List CycleWitness)) × Nat =>
      (⟨q.1.2.1, q.2 + 1⟩ : CycleWitness) :=
    primrec_mk.comp (Primrec.fst.comp (Primrec.snd.comp Primrec.fst))
      (Primrec.succ.comp Primrec.snd)
  have hrange : Primrec fun q : Nat × (Nat × List CycleWitness) =>
      List.range (q.1 - q.2.1) :=
    Primrec.list_range.comp (Primrec.nat_sub.comp Primrec.fst
      (Primrec.fst.comp Primrec.snd))
  have hmap : Primrec fun q : Nat × (Nat × List CycleWitness) =>
      (List.range (q.1 - q.2.1)).map fun k => (⟨q.2.1, k + 1⟩ : CycleWitness) :=
    Primrec.list_map hrange hinner
  have hstep : Primrec₂ fun (n : Nat) (p : Nat × List CycleWitness) =>
      ((List.range (n - p.1)).map fun k => (⟨p.1, k + 1⟩ : CycleWitness)) ++ p.2 :=
    Primrec.list_append.comp hmap (Primrec.snd.comp Primrec.snd)
  have hfold : Primrec fun n : Nat =>
      (List.range n).foldr
        (fun m acc => ((List.range (n - m)).map fun k =>
          (⟨m, k + 1⟩ : CycleWitness)) ++ acc) [] :=
    Primrec.list_foldr Primrec.list_range (Primrec.const []) hstep
  exact hfold.of_eq (fun n => by rw [cycleCandidates, flatMap_eq_foldr])


end TamesisLab.Foundations.UniformPrimrec
