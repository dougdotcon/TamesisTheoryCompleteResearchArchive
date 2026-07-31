import TamesisLab.Benchmark

/-!
# LAB-BENCH-001 — teste de importação e referência

Importa todos os módulos do benchmark e verifica que cada definição e cada
teorema podem ser referenciados com suas assinaturas. Benchmark de
infraestrutura; valor científico: NONE — INFRASTRUCTURE BENCHMARK.

Rastreabilidade: 05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md
(BENCH-TEST-001).
-/

namespace TamesisLab.Tests.Benchmark

open TamesisLab.Benchmark

universe u v w x

-- BENCH-FUN-001: identidade e composição de funções.
example {α : Type u} {β : Type v} {γ : Type w} {δ : Type x}
    (h : γ → δ) (g : β → γ) (f : α → β) :
    fcomp (fcomp h g) f = fcomp h (fcomp g f) := fcomp_assoc h g f

example {α : Type u} {β : Type v} (f : α → β) : fcomp fid f = f :=
  fcomp_fid_left f

example {α : Type u} {β : Type v} (f : α → β) : fcomp f fid = f :=
  fcomp_fid_right f

-- BENCH-DEF-001: regimes, ciclo determinístico, estado e transição tipada.
example (r : Regime) : r.step.step.step = r := Regime.step_cycle r

example (r : Regime) : (BenchState.init r).regime = r :=
  BenchState.init_regime r

example (r : Regime) : (BenchState.init r).tick = 0 :=
  BenchState.init_tick r

example {α : Type u} (t s r : Transition α) :
    (t.comp s).comp r = t.comp (s.comp r) := Transition.comp_assoc t s r

example {α : Type u} (t : Transition α) : (Transition.id α).comp t = t :=
  Transition.id_comp t

example {α : Type u} (t : Transition α) : t.comp (Transition.id α) = t :=
  Transition.comp_id t

-- BENCH-REL-001: composição relacional e relação declarada.
example {α : Type u} (R S T : BRel α) :
    rcomp (rcomp R S) T = rcomp R (rcomp S T) := rcomp_assoc R S T

example {α : Type u} (R : BRel α) : rcomp rid R = R := rcomp_rid_left R

example {α : Type u} (R : BRel α) : rcomp R rid = R := rcomp_rid_right R

example (r : Regime) : Regime.Adj r r.step := Regime.step_adj r

-- BENCH-MATHLIB-001: uso controlado de Mathlib.
example : Regime.alpha ∈ ({Regime.alpha} : Finset Regime) :=
  alpha_mem_singleton

example : Regime.beta ∉ ({Regime.alpha} : Finset Regime) :=
  beta_not_mem_singleton

end TamesisLab.Tests.Benchmark
