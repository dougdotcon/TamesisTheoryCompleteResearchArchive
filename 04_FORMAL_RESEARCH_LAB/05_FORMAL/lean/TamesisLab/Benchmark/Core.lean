/-!
# LAB-BENCH-001 — Core: identidade e composição de funções

Benchmark de infraestrutura. Todos os resultados deste arquivo são fatos
elementares e conhecidos sobre composição de funções. Valor científico:
NONE — INFRASTRUCTURE BENCHMARK. Nenhum resultado do Programa Tamesis é
usado como premissa.

A composição e a identidade são definidas localmente para que o benchmark
teste a construção local, e não a reutilização de lemas prontos da Mathlib.

Rastreabilidade: 05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md
(BENCH-FUN-001).
-/

namespace TamesisLab.Benchmark

universe u v w x

/-- Composição de funções definida localmente para o benchmark. -/
def fcomp {α : Type u} {β : Type v} {γ : Type w} (g : β → γ) (f : α → β) :
    α → γ :=
  fun a => g (f a)

/-- Função identidade definida localmente para o benchmark. -/
def fid {α : Type u} : α → α := fun a => a

/-- Associatividade da composição de funções. Resultado conhecido. -/
theorem fcomp_assoc {α : Type u} {β : Type v} {γ : Type w} {δ : Type x}
    (h : γ → δ) (g : β → γ) (f : α → β) :
    fcomp (fcomp h g) f = fcomp h (fcomp g f) := rfl

/-- Identidade à esquerda para a composição. Resultado conhecido. -/
theorem fcomp_fid_left {α : Type u} {β : Type v} (f : α → β) :
    fcomp fid f = f := rfl

/-- Identidade à direita para a composição. Resultado conhecido. -/
theorem fcomp_fid_right {α : Type u} {β : Type v} (f : α → β) :
    fcomp f fid = f := rfl

end TamesisLab.Benchmark
