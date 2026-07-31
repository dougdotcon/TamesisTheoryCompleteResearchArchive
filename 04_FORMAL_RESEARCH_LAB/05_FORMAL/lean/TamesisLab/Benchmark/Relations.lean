import TamesisLab.Benchmark.Structures

/-!
# LAB-BENCH-001 — Relations: relação finita e composição relacional

Benchmark de infraestrutura. Este arquivo define uma relação finita explícita
entre os regimes do benchmark, separada da função determinística `Regime.step`,
e uma composição relacional local com identidade e associatividade. Todos os
teoremas são fatos elementares e conhecidos. Valor científico:
NONE — INFRASTRUCTURE BENCHMARK. Nenhum resultado do Programa Tamesis é usado
como premissa.

Rastreabilidade: 05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md
(BENCH-REL-001).
-/

namespace TamesisLab.Benchmark

universe u

/-- Relação binária sobre `α`. Abreviação local do benchmark. -/
def BRel (α : Type u) : Type u := α → α → Prop

/-- Composição relacional definida localmente para o benchmark. -/
def rcomp {α : Type u} (R S : BRel α) : BRel α :=
  fun a c => ∃ b, R a b ∧ S b c

/-- Relação identidade (diagonal). -/
def rid {α : Type u} : BRel α := fun a b => a = b

/-- Associatividade da composição relacional. Resultado conhecido. -/
theorem rcomp_assoc {α : Type u} (R S T : BRel α) :
    rcomp (rcomp R S) T = rcomp R (rcomp S T) := by
  funext a d
  apply propext
  constructor
  · intro h
    match h with
    | ⟨c, ⟨b, hab, hbc⟩, hcd⟩ => exact ⟨b, hab, c, hbc, hcd⟩
  · intro h
    match h with
    | ⟨b, hab, c, hbc, hcd⟩ => exact ⟨c, ⟨b, hab, hbc⟩, hcd⟩

/-- Identidade à esquerda para a composição relacional. Resultado conhecido. -/
theorem rcomp_rid_left {α : Type u} (R : BRel α) : rcomp rid R = R := by
  funext a c
  apply propext
  constructor
  · intro h
    match h with
    | ⟨b, hab, hbc⟩ => cases hab; exact hbc
  · intro h
    exact ⟨a, rfl, h⟩

/-- Identidade à direita para a composição relacional. Resultado conhecido. -/
theorem rcomp_rid_right {α : Type u} (R : BRel α) : rcomp R rid = R := by
  funext a c
  apply propext
  constructor
  · intro h
    match h with
    | ⟨b, hab, hbc⟩ => cases hbc; exact hab
  · intro h
    exact ⟨c, h, rfl⟩

/-- Relação de adjacência declarada entre os regimes do benchmark.
Definida por casos explícitos, separada da função `Regime.step`. -/
inductive Regime.Adj : Regime → Regime → Prop
  | alphaBeta : Regime.Adj .alpha .beta
  | betaGamma : Regime.Adj .beta .gamma
  | gammaAlpha : Regime.Adj .gamma .alpha

/-- A transição determinística respeita a relação declarada.
Prova por análise finita dos casos. Resultado conhecido. -/
theorem Regime.step_adj (r : Regime) : Regime.Adj r r.step := by
  cases r <;> constructor

end TamesisLab.Benchmark
