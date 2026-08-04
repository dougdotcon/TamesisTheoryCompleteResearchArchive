import TamesisLab.Foundations.UniformPrimrec.Execution

set_option autoImplicit false

/-!
# FOUND-UNIFORM-PRIMREC-001 — o casamento

`RawValid` tem as **mesmas quatro clausulas, na mesma ordem e no mesmo
aninhamento** de `CycleWitness.Valid`. E isso que torna
`valid_iff_rawValid` um transporte, e nao uma prova nova.

`detectCycle?_eq_raw` **nao reimplementa** o detector: mostra que o
detector ja existente e igual a um `find?` sobre a mesma lista de
candidatos com um predicado equivalente.
-/

namespace TamesisLab.Foundations.UniformPrimrec

open TamesisLab.Engineering.FiniteStateRuntime
open TamesisLab.Foundations.CycleDetection
open TamesisLab.Foundations.ComputabilityBridge

def RawValid (raw : RawTransitionTable) (start : Nat) (w : CycleWitness) : Prop :=
  w.baseIndex < raw.next.size ∧ 0 < w.period ∧
    w.baseIndex + w.period ≤ raw.next.size ∧
      raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start

def rawValidBool (raw : RawTransitionTable) (start : Nat) (w : CycleWitness) : Bool :=
  if w.baseIndex < raw.next.size then
    if 0 < w.period then
      if w.baseIndex + w.period ≤ raw.next.size then
        if raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start then
          true else false
      else false
    else false
  else false

theorem rawValidBool_iff (raw : RawTransitionTable) (start : Nat) (w : CycleWitness) :
    rawValidBool raw start w = true ↔ RawValid raw start w := by
  unfold rawValidBool RawValid
  by_cases h1 : w.baseIndex < raw.next.size
  · by_cases h2 : 0 < w.period
    · by_cases h3 : w.baseIndex + w.period ≤ raw.next.size
      · by_cases h4 : raw.run? (w.baseIndex + w.period) start = raw.run? w.baseIndex start
        · simp [h1, h2, h3, h4]
        · simp [h1, h2, h3, h4]
      · simp [h1, h2, h3]
    · simp [h1, h2]
  · simp [h1]

theorem primrec_rawValidBool :
    Primrec fun q : (RawTransitionTable × Nat) × CycleWitness =>
      rawValidBool q.1.1 q.1.2 q.2 := by
  have hraw : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness => q.1.1 :=
    Primrec.fst.comp Primrec.fst
  have hstart : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness => q.1.2 :=
    Primrec.snd.comp Primrec.fst
  have hb : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness => q.2.baseIndex :=
    primrec_baseIndex.comp Primrec.snd
  have hp : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness => q.2.period :=
    primrec_period.comp Primrec.snd
  have hsize : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness =>
      q.1.1.next.size := primrec_size.comp hraw
  have hsum : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness =>
      q.2.baseIndex + q.2.period := Primrec.nat_add.comp hb hp
  have hrun1 : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness =>
      q.1.1.run? (q.2.baseIndex + q.2.period) q.1.2 :=
    primrec_run?_gen hraw hsum hstart
  have hrun2 : Primrec fun q : (RawTransitionTable × Nat) × CycleWitness =>
      q.1.1.run? q.2.baseIndex q.1.2 := primrec_run?_gen hraw hb hstart
  exact Primrec.ite (Primrec.nat_lt.comp hb hsize)
    (Primrec.ite (Primrec.nat_lt.comp (Primrec.const 0) hp)
      (Primrec.ite (Primrec.nat_le.comp hsum hsize)
        (Primrec.ite (Primrec.eq.comp hrun1 hrun2)
          (Primrec.const true) (Primrec.const false))
        (Primrec.const false))
      (Primrec.const false))
    (Primrec.const false)


theorem valid_iff_rawValid (t : ValidatedTransitionTable)
    (start : Fin t.next.size) (w : CycleWitness) :
    CycleWitness.Valid t.step start w ↔ RawValid t.toRaw (start : Nat) w := by
  unfold CycleWitness.Valid RawValid
  rw [Fintype.card_fin]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨h1, h2, h3, ?_⟩
    rw [t.run?_eq_iterate_step (w.baseIndex + w.period) start,
        t.run?_eq_iterate_step w.baseIndex start, h4]
  · rintro ⟨h1, h2, h3, h4⟩
    refine ⟨h1, h2, h3, ?_⟩
    rw [t.run?_eq_iterate_step (w.baseIndex + w.period) start,
        t.run?_eq_iterate_step w.baseIndex start] at h4
    exact Fin.ext (Option.some.inj h4)

theorem detectCycle?_eq_raw (t : ValidatedTransitionTable) (start : Fin t.next.size) :
    t.detectCycle? start =
      (cycleCandidates t.next.size).find?
        (fun w => rawValidBool t.toRaw (start : Nat) w) := by
  show detectCycleWitness? t.step start = _
  unfold detectCycleWitness?
  rw [Fintype.card_fin]
  congr 1
  funext w
  by_cases h : RawValid t.toRaw (start : Nat) w
  · rw [decide_eq_true ((valid_iff_rawValid t start w).mpr h),
      (rawValidBool_iff _ _ w).mpr h]
  · have h1 : ¬ CycleWitness.Valid t.step start w :=
      fun hc => h ((valid_iff_rawValid t start w).mp hc)
    have h2 : rawValidBool t.toRaw (start : Nat) w = false :=
      Bool.eq_false_iff.mpr (fun hc => h ((rawValidBool_iff _ _ w).mp hc))
    rw [decide_eq_false h1, h2]


end TamesisLab.Foundations.UniformPrimrec
