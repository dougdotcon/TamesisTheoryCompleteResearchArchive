import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics

/-!
# RH-NOGO-001 — SignatureProbe

Probe de assinaturas para o núcleo abstrato ASYM-NOGO-001
(`03_MILLENNIUM/01_RIEMANN/ASYMPTOTIC_CORE.md`).

Este arquivo registra o **enunciado** candidato como `Prop`. Foi criado no
gate de especificação sem corpo probatório, apenas para verificar que a
assinatura elabora contra a Mathlib fixada e que as ferramentas
assintóticas previstas existem — verificação que já corrigiu um erro de
namespace (`isLittleO_log_rpow_atTop` está no namespace raiz) antes de
qualquer tentativa de prova.

Atualização (gate ASYM-NOGO-001, 2026-07-31): o enunciado passou a ser
**provado** em `TamesisLab/RHNogo/AsymptoticCore/Audit.lean`
(`TamesisLab.RHNogo.asymNogoStatement_holds`). Este arquivo permanece como
registro histórico da assinatura e das ferramentas verificadas.

Nada neste arquivo constrói operador espectral, usa zeros da zeta, assume a
Hipótese de Riemann ou constitui progresso sobre ela.
-/

namespace TamesisLab.RHNogo

open Filter

/-- Enunciado candidato ASYM-NOGO-001: nenhuma função real satisfaz
simultaneamente uma assintótica `c · T log T` com `c > 0` e uma assintótica
`C · T ^ α` com `C, α > 0`. Provado em
`AsymptoticCore/Audit.lean`. -/
def AsymNogoStatement : Prop :=
  ∀ (N : ℝ → ℝ) (c C α : ℝ), 0 < c → 0 < C → 0 < α →
    Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c) →
    ¬ Tendsto (fun T => N T / T ^ α) atTop (nhds C)

-- Ferramentas Mathlib verificadas por elaboração (nenhum teorema é provado
-- neste arquivo).
#check (Real.tendsto_log_atTop : Tendsto Real.log atTop atTop)
#check @isLittleO_log_rpow_atTop
#check @tendsto_rpow_atTop
#check @Asymptotics.IsBigO
#check @Asymptotics.IsLittleO
#check @tendsto_nhds_unique
#check @Filter.Tendsto.div

end TamesisLab.RHNogo
