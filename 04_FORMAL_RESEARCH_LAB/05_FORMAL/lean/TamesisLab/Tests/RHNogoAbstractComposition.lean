import TamesisLab.RHNogo.Composition

set_option autoImplicit false

/-!
# Teste isolado — ABSTRACT-NOGO-001

Confirma as assinaturas do teorema principal e dos corolários.

**Não** constrói exemplos concretos: qualquer instância seria por
construção impossível (as três hipóteses são contraditórias), e exibi-la
exigiria `False.elim` ou uma hipótese falsa — o que esconderia, em vez de
verificar, o conteúdo. **Não** se usa `ex falso` em lugar algum: tudo
abaixo é confirmação de tipo a partir de hipóteses genéricas.
-/

namespace TamesisLab.Tests.RHNogoAbstractComposition

open Filter TamesisLab.RHNogo.Bridge TamesisLab.RHNogo.Composition

/-- ABSTRACT-NOGO-001 — assinatura do teorema principal. -/
example : ∀ (NTarget NBase : ℝ → ℝ),
    PowerCountingLaw NTarget →
    TLogCountingLaw NBase →
    SubdominantTLog NTarget NBase →
    False :=
  fun _ _ hP hT hS => abstract_power_tlog_incompatibility hP hT hS

/-- O enunciado registrado coincide com a assinatura. -/
example : AbstractNogoStatement := abstractNogoStatement_holds

/-- A estrutura agregadora é inabitável. -/
example (NTarget NBase : ℝ → ℝ)
    (h : AbstractCountingNogoData NTarget NBase) : False :=
  h.false

/-- Reciprocamente, os três dados constroem a estrutura — confirmando que
os campos têm exatamente os tipos das três hipóteses. -/
example (NTarget NBase : ℝ → ℝ)
    (hP : PowerCountingLaw NTarget) (hT : TLogCountingLaw NBase)
    (hS : SubdominantTLog NTarget NBase) : False :=
  AbstractCountingNogoData.false
    { powerLaw := hP, tLogLaw := hT, subdominant := hS }

/-- ABSTRACT-NOGO-E0-001 — assinatura do corolário de igualdade eventual. -/
example : ∀ (NTarget NBase : ℝ → ℝ),
    PowerCountingLaw NTarget →
    TLogCountingLaw NBase →
    NTarget =ᶠ[atTop] NBase →
    False :=
  fun _ _ hP hT hEq => abstract_nogo_of_eventuallyEq hP hT hEq

/-- ABSTRACT-NOGO-E1-001 — assinatura do corolário de diferença limitada. -/
example : ∀ (NTarget NBase : ℝ → ℝ),
    PowerCountingLaw NTarget →
    TLogCountingLaw NBase →
    BoundedDifference NTarget NBase →
    False :=
  fun _ _ hP hT hB => abstract_nogo_of_boundedDifference hP hT hB

/-- Confirmação da **direção da diferença**: `SubdominantTLog X Y` é
literalmente `X − Y = o(T log T)`, não a orientação inversa. -/
example (NTarget NBase : ℝ → ℝ) :
    SubdominantTLog NTarget NBase ↔
      (fun T => NTarget T - NBase T)
        =o[atTop] (fun T : ℝ => T * Real.log T) :=
  Iff.rfl

/-- A constante `T log T` é preservada pela transferência usada no passo 1
da prova — verificado por `rfl`. -/
example (NTarget NBase : ℝ → ℝ) (hT : TLogCountingLaw NBase)
    (hS : SubdominantTLog NTarget NBase) :
    (TLogCountingLaw.transfer hT hS).constant = hT.constant := rfl

end TamesisLab.Tests.RHNogoAbstractComposition
