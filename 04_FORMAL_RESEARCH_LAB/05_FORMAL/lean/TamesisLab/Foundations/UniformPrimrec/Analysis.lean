import TamesisLab.Foundations.UniformPrimrec.Validity
import TamesisLab.Foundations.UniformPrimrec.Candidates
import TamesisLab.Foundations.UniformPrimrec.Witness

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — o fechamento

O fechamento e `primrec_analyzeTransitionTable`, que afirma
`Primrec₂` da analise de tabelas.

Sobre `RawTransitionTable × Nat` o dominio e **infinito**,
`Primrec.dom_finite` nao se aplica, e a prova **consulta o algoritmo**.
Fecha `CB-GAP-001`.

**`Primrec` nao significa eficiente.** A classe contem torres de
exponenciais, e esta frente nao enuncia cota nenhuma — ver `UP-GAP-003`.

A reducao do bloco `do` vem de `analyzeTransitionTable_reduce`, publica
desde `ENG-RUNTIME-SOUNDNESS-002`. Antes dela esta frente mantinha a
**quarta** copia privada da mesma reducao — `UP-GAP-002`, fechada.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

def analyzeRaw (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness :=
  if validBool raw = true then
    if start < raw.next.size then
      match (cycleCandidates raw.next.size).find?
          (fun w => rawValidBool raw start w) with
      | some w => .ok w
      | none => .error .internalDetectorFailure
    else .error (.initialStateOutOfBounds start raw.next.size)
  else .error .transitionDestinationOutOfBounds

theorem analyzeRaw_eq (raw : RawTransitionTable) (start : Nat) :
    analyzeRaw raw start = analyzeTransitionTable raw start := by
  unfold analyzeRaw
  by_cases hRaw : raw.Valid
  · have hvb : validBool raw = true := (validBool_iff raw).mpr hRaw
    by_cases hStart : start < raw.next.size
    · rw [if_pos hvb, if_pos hStart, analyzeTransitionTable_reduce hRaw hStart,
        detectCycle?_eq_raw (⟨raw.next, hRaw⟩ : ValidatedTransitionTable)
          ⟨start, hStart⟩]
      rfl
    · rw [if_pos hvb, if_neg hStart,
        analyzeTransitionTable_invalid_start raw start hRaw hStart]
  · have hvb : ¬ (validBool raw = true) := fun hc => hRaw ((validBool_iff raw).mp hc)
    rw [if_neg hvb, analyzeTransitionTable_invalid_table raw start hRaw]



theorem primrec_ok :
    Primrec fun w : CycleWitness =>
      (Except.ok w : Except RuntimeCycleError CycleWitness) := by
  have h : Primrec fun s : RuntimeCycleError ⊕ CycleWitness =>
      (exceptEquiv RuntimeCycleError CycleWitness).symm s :=
    Primrec.of_equiv_symm (e := exceptEquiv RuntimeCycleError CycleWitness)
  exact (h.comp Primrec.sumInr).of_eq (fun _ => rfl)

theorem primrec_error :
    Primrec fun e : RuntimeCycleError =>
      (Except.error e : Except RuntimeCycleError CycleWitness) := by
  have h : Primrec fun s : RuntimeCycleError ⊕ CycleWitness =>
      (exceptEquiv RuntimeCycleError CycleWitness).symm s :=
    Primrec.of_equiv_symm (e := exceptEquiv RuntimeCycleError CycleWitness)
  exact (h.comp Primrec.sumInl).of_eq (fun _ => rfl)

theorem primrec_initialStateOutOfBounds :
    Primrec fun p : Nat × Nat =>
      RuntimeCycleError.initialStateOutOfBounds p.1 p.2 := by
  have h : Primrec fun s : Bool ⊕ (Nat × Nat) => runtimeCycleErrorEquiv.symm s :=
    Primrec.of_equiv_symm (e := runtimeCycleErrorEquiv)
  exact (h.comp Primrec.sumInr).of_eq (fun _ => rfl)

theorem primrec_find :
    Primrec fun p : RawTransitionTable × Nat =>
      (cycleCandidates p.1.next.size).find? (fun w => rawValidBool p.1 p.2 w) := by
  have hcand : Primrec fun p : RawTransitionTable × Nat =>
      cycleCandidates p.1.next.size :=
    primrec_cycleCandidates.comp (primrec_size.comp Primrec.fst)
  have hidx : Primrec fun p : RawTransitionTable × Nat =>
      List.findIdx (fun w => rawValidBool p.1 p.2 w)
        (cycleCandidates p.1.next.size) :=
    Primrec.list_findIdx hcand primrec_rawValidBool
  exact (Primrec.list_getElem?.comp hcand hidx).of_eq
    (fun _ => (List.find?_eq_getElem?_findIdx).symm)

/-- **O FECHAMENTO.** A analise de tabelas e primitiva recursiva sobre um
dominio INFINITO. Nao por finitude — a prova consulta o algoritmo. -/
theorem primrec_analyzeRaw : Primrec₂ analyzeRaw := by
  have hvalid : PrimrecPred fun p : RawTransitionTable × Nat =>
      validBool p.1 = true :=
    Primrec.eq.comp (primrec_validBool.comp Primrec.fst) (Primrec.const true)
  have hsize : Primrec fun p : RawTransitionTable × Nat => p.1.next.size :=
    primrec_size.comp Primrec.fst
  have hstart : PrimrecPred fun p : RawTransitionTable × Nat =>
      p.2 < p.1.next.size := Primrec.nat_lt.comp Primrec.snd hsize
  have herr : Primrec fun p : RawTransitionTable × Nat =>
      (Except.error (RuntimeCycleError.initialStateOutOfBounds p.2 p.1.next.size)
        : Except RuntimeCycleError CycleWitness) :=
    primrec_error.comp (primrec_initialStateOutOfBounds.comp
      (Primrec.snd.pair hsize))
  have hmatch : Primrec fun p : RawTransitionTable × Nat =>
      (match (cycleCandidates p.1.next.size).find?
          (fun w => rawValidBool p.1 p.2 w) with
        | some w => (Except.ok w : Except RuntimeCycleError CycleWitness)
        | none => .error .internalDetectorFailure) := by
    refine (Primrec.option_casesOn primrec_find
      (Primrec.const (Except.error RuntimeCycleError.internalDetectorFailure
        : Except RuntimeCycleError CycleWitness))
      (primrec_ok.comp Primrec.snd).to₂).of_eq (fun p => ?_)
    cases (cycleCandidates p.1.next.size).find?
        (fun w => rawValidBool p.1 p.2 w) <;> rfl
  exact Primrec.ite hvalid (Primrec.ite hstart hmatch herr)
    (Primrec.const (Except.error RuntimeCycleError.transitionDestinationOutOfBounds
      : Except RuntimeCycleError CycleWitness))

/-- **CB-GAP-001 fechada.** -/
theorem primrec_analyzeTransitionTable : Primrec₂ analyzeTransitionTable :=
  primrec_analyzeRaw.of_eq analyzeRaw_eq

/-- O enunciado que a ponte deixou registrado e nao provou. -/
theorem uniformPrimrecStatement_holds : UniformPrimrecStatement :=
  primrec_analyzeTransitionTable



end TamesisLab.Foundations.UniformPrimrec
