import TamesisLab.Foundations.UniformPrimrec.Execution

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — validade da tabela

`validBool` usa `if` e nao `decide` **de proposito**: `PrimrecPred`
carrega a sua propria instancia de `DecidablePred`, e misturar as duas
formas produz incompatibilidade que nenhuma tatica desfaz. Ver
`STOP-UP-005`.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

def validBool (raw : RawTransitionTable) : Bool :=
  (raw.next.toList).foldr
    (fun x s => if x < raw.next.toList.length then s else false) true

theorem foldr_lt_eq_true (n : Nat) :
    ∀ l : List Nat,
      (l.foldr (fun x s => if x < n then s else false) true = true) ↔ ∀ x ∈ l, x < n := by
  intro l
  induction l with
  | nil => simp
  | cons a l ih =>
      rw [List.foldr_cons]
      by_cases h : a < n
      · rw [if_pos h, ih]
        constructor
        · intro hl x hx
          rcases List.mem_cons.mp hx with rfl | hx'
          · exact h
          · exact hl x hx'
        · intro hl x hx
          exact hl x (List.mem_cons_of_mem _ hx)
      · rw [if_neg h]
        constructor
        · intro hf; simp at hf
        · intro hl; exact absurd (hl a (by simp)) h

theorem validBool_iff (raw : RawTransitionTable) :
    validBool raw = true ↔ raw.Valid := by
  unfold validBool RawTransitionTable.Valid
  rw [foldr_lt_eq_true]
  constructor
  · intro h i
    have hm : raw.next.toList[(i : Nat)]'(by simp) ∈ raw.next.toList :=
      List.getElem_mem _
    have hx := h _ hm
    simpa using hx
  · intro h x hx
    obtain ⟨i, hi, rfl⟩ := List.mem_iff_getElem.mp hx
    have hi' : i < raw.next.size := by simpa using hi
    have := h ⟨i, hi'⟩
    simpa using this

theorem primrec_validBool : Primrec validBool := by
  have hc : PrimrecPred fun a : RawTransitionTable × (Nat × Bool) =>
      a.2.1 < a.1.next.toList.length :=
    Primrec.nat_lt.comp (Primrec.fst.comp Primrec.snd)
      (Primrec.list_length.comp (primrec_next_toList.comp Primrec.fst))
  have h : Primrec₂ fun (raw : RawTransitionTable) (p : Nat × Bool) =>
      (if p.1 < raw.next.toList.length then p.2 else false) :=
    Primrec.ite hc (Primrec.snd.comp Primrec.snd) (Primrec.const false)
  exact (Primrec.list_foldr primrec_next_toList (Primrec.const true) h).of_eq
    (fun _ => rfl)


end TamesisLab.Foundations.UniformPrimrec
