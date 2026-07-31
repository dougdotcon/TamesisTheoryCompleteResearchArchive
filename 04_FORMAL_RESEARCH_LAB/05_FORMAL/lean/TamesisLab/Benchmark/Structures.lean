import TamesisLab.Benchmark.Core

/-!
# LAB-BENCH-001 — Structures: regimes finitos, estado e transição tipada

Benchmark de infraestrutura. Os objetos deste arquivo são fixtures de
benchmark: um tipo enumerado com três regimes, uma função cíclica
determinística, uma estrutura pequena de estado e um wrapper tipado de
transformação com composição e identidade. Todos os teoremas são fatos
elementares e conhecidos. Valor científico: NONE — INFRASTRUCTURE BENCHMARK.
Isto não define uma teoria geral de regimes e não usa resultados do
Programa Tamesis como premissas.

Rastreabilidade: 05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md
(BENCH-DEF-001, BENCH-FUN-001).
-/

namespace TamesisLab.Benchmark

universe u

/-- Tipo enumerado finito com três regimes. Fixture de benchmark. -/
inductive Regime where
  | alpha
  | beta
  | gamma
deriving DecidableEq, Repr

/-- Transição determinística cíclica: `alpha → beta → gamma → alpha`. -/
def Regime.step : Regime → Regime
  | .alpha => .beta
  | .beta  => .gamma
  | .gamma => .alpha

/-- Aplicar a transição três vezes retorna ao regime inicial.
Prova por análise finita dos casos. Resultado conhecido. -/
theorem Regime.step_cycle (r : Regime) : r.step.step.step = r := by
  cases r <;> rfl

/-- Estrutura pequena de estado: um regime e um contador. Fixture. -/
structure BenchState where
  regime : Regime
  tick : Nat
deriving DecidableEq, Repr

/-- Construtor canônico do estado inicial. -/
def BenchState.init (r : Regime) : BenchState := ⟨r, 0⟩

/-- Projeção do regime após a construção. Resultado conhecido. -/
theorem BenchState.init_regime (r : Regime) :
    (BenchState.init r).regime = r := rfl

/-- Projeção do contador após a construção. Resultado conhecido. -/
theorem BenchState.init_tick (r : Regime) :
    (BenchState.init r).tick = 0 := rfl

/-- Wrapper tipado de uma transformação `α → α`. Fixture de benchmark. -/
structure Transition (α : Type u) where
  apply : α → α

/-- Transição identidade. -/
def Transition.id (α : Type u) : Transition α := ⟨fid⟩

/-- Composição de transições, via a composição local `fcomp`. -/
def Transition.comp {α : Type u} (t s : Transition α) : Transition α :=
  ⟨fcomp t.apply s.apply⟩

/-- Associatividade da composição de transições. Resultado conhecido. -/
theorem Transition.comp_assoc {α : Type u} (t s r : Transition α) :
    (t.comp s).comp r = t.comp (s.comp r) := rfl

/-- Identidade à esquerda. Resultado conhecido. -/
theorem Transition.id_comp {α : Type u} (t : Transition α) :
    (Transition.id α).comp t = t := rfl

/-- Identidade à direita. Resultado conhecido. -/
theorem Transition.comp_id {α : Type u} (t : Transition α) :
    t.comp (Transition.id α) = t := rfl

end TamesisLab.Benchmark
