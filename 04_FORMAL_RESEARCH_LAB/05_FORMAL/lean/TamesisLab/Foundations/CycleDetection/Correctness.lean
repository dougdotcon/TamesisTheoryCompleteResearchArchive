import TamesisLab.Foundations.CycleDetection.Detector
import TamesisLab.Foundations.FiniteDynamics.EventualPeriodicity

set_option autoImplicit false

/-!
# FOUND-CYCLE-DETECTION-001 — Correção e completude

## Soundness

As três cotas vivem **dentro** de `CycleWitness.Valid`, de modo que a
correção sai do predicado decidido, sem consultar a lista.
`mem_cycleCandidates_iff` **não** é dependência aqui — e isso é uma
fortificação: a soundness sobrevive a uma troca de algoritmo.

## Completeness

Transporte direto de `FiniteDynamics.exists_bounded_iterate_collision`,
cuja conclusão é literalmente o contrato do certificado. A casa dos pombos
foi consumida **uma única vez**, naquele teorema, e **não** é repetida
aqui — o lema de contagem da Mathlib que a implementa não é invocado em
nenhum ponto desta frente, e a auditoria em `PROOF_AUDIT.md` exige
contagem zero para ele.

A completude garante que `detectCycleWitness?` nunca devolve `none` quando
chamada sobre um tipo finito habitado por `x`. A API continua devolvendo
`Option` porque a totalização não faz parte desta versão.
-/

namespace TamesisLab.Foundations.CycleDetection

open TamesisLab.Foundations.FiniteDynamics

/-- **Soundness**: o certificado devolvido satisfaz o contrato. -/
theorem detectCycleWitness?_sound {X : Type*} [Fintype X] [DecidableEq X]
    {f : X → X} {x : X} {w : CycleWitness}
    (h : detectCycleWitness? f x = some w) :
    CycleWitness.Valid f x w := by
  unfold detectCycleWitness? at h
  exact of_decide_eq_true
    (List.find?_some (p := fun v => decide (CycleWitness.Valid f x v)) h)

/-- **Completeness**: alguma testemunha é sempre devolvida.

Reutiliza `exists_bounded_iterate_collision`. Não se afirma que a
testemunha devolvida coincide com a produzida pelo teorema existencial. -/
theorem detectCycleWitness?_complete {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    ∃ w : CycleWitness, detectCycleWitness? f x = some w := by
  obtain ⟨mu, lam, hmu, hlam, hsum, hcol⟩ :=
    exists_bounded_iterate_collision f x
  have hvalid : CycleWitness.Valid f x ⟨mu, lam⟩ := ⟨hmu, hlam, hsum, hcol⟩
  have hmem : (⟨mu, lam⟩ : CycleWitness) ∈ cycleCandidates (Fintype.card X) :=
    mem_cycleCandidates_iff.mpr ⟨hmu, hlam, hsum⟩
  have hsome : (detectCycleWitness? f x).isSome = true := by
    unfold detectCycleWitness?
    exact List.find?_isSome.mpr ⟨⟨mu, lam⟩, hmem, by simpa using hvalid⟩
  exact Option.isSome_iff_exists.mp hsome

end TamesisLab.Foundations.CycleDetection
