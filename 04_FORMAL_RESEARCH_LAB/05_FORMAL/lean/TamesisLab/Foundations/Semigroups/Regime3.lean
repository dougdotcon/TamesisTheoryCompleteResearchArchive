import Mathlib.Data.Finset.Insert
import Mathlib.Data.Fintype.Defs

/-!
# FOUND-SEMIGROUP-001 — Regime3: modelo cíclico finito

Camada B do gate: três regimes e três transições, definidos localmente e
independentes das fixtures do LAB-BENCH-001 (redefinição independente,
opção B da seção 8 do gate).

Convenção de composição: `Shift3.comp a b` aplica `b` primeiro e depois `a`,
alinhada à lei `mul_smul` da Mathlib. Ver `Basic.lean` e `DEFINITIONS.md`.

O fechamento (FOUND-SG-001) é garantido por construção: `Shift3.comp` tem
contradomínio `Shift3` por tipagem. Isto é registrado como propriedade
estrutural, não como teorema profundo.

Valor científico: FOUNDATIONAL_FORMALIZATION_ONLY. Modelo finito concreto,
sem pretensão de universalidade.
-/

namespace TamesisLab.Foundations.Semigroups

/-- Três regimes. Instância concreta finita; nenhum significado físico. -/
inductive Regime3 where
  | alpha
  | beta
  | gamma
deriving DecidableEq, Repr

/-- Enumeração finita explícita dos três regimes. Instância manual porque o
derive handler de `Fintype` da revisão fixada falha sob imports mínimos. -/
instance : Fintype Regime3 where
  elems := {.alpha, .beta, .gamma}
  complete := fun x => by cases x <;> decide

/-- Três transições determinísticas sobre `Regime3`: a identidade, o avanço
cíclico e o avanço cíclico duplo. -/
inductive Shift3 where
  | identity
  | forward
  | forward2
deriving DecidableEq, Repr

/-- Enumeração finita explícita das três transições. Instância manual pela
mesma razão registrada em `Regime3`. -/
instance : Fintype Shift3 where
  elems := {.identity, .forward, .forward2}
  complete := fun x => by cases x <;> decide

/-- Ação de uma transição sobre um regime. Determinística e total. -/
def Shift3.apply : Shift3 → Regime3 → Regime3
  | .identity, r => r
  | .forward, .alpha => .beta
  | .forward, .beta => .gamma
  | .forward, .gamma => .alpha
  | .forward2, .alpha => .gamma
  | .forward2, .beta => .alpha
  | .forward2, .gamma => .beta

/-- Composição de transições: `comp a b` aplica `b` primeiro e depois `a`.
FOUND-SG-001: o fechamento é garantido por construção pelo tipo de retorno. -/
def Shift3.comp : Shift3 → Shift3 → Shift3
  | .identity, s => s
  | .forward, .identity => .forward
  | .forward, .forward => .forward2
  | .forward, .forward2 => .identity
  | .forward2, .identity => .forward2
  | .forward2, .forward => .identity
  | .forward2, .forward2 => .forward

end TamesisLab.Foundations.Semigroups
