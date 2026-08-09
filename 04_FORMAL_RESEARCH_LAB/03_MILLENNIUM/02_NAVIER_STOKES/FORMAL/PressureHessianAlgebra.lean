/-
NS-PRESSURE-001 — rascunho isolado, NÃO integrado a `TamesisLab.lean`.

STATUS: COMPILADO na integração serial pela sessão orquestradora, via
`lake env lean` (fora do rascunho paralelo original, que corretamente
não rodou `lake build` — ver
`04_FORMAL_RESEARCH_LAB/01_PORTFOLIO/PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`).
`exit 0`. Duas correções foram necessárias no rascunho original:
`linarith` exigia `import Mathlib.Tactic.Linarith` (não estava entre os
quatro imports específicos escolhidos); `ring` na linha `expand` falhou
porque `Matrix n n ℝ` não é comutativa — trocado por `noncomm_ring`
(`import Mathlib.Tactic.NoncommRing`). `#print axioms` em ambos os
teoremas: `[propext, Classical.choice, Quot.sound]`, a pegada padrão do
laboratório. Ainda NÃO registrado em `TamesisLab.lean` — arquivo
autônomo fora da árvore de import do projeto.

Nenhuma prova incompleta nem premissa não justificada foi usada — se
algum passo abaixo não fechar ao compilar de fato, o gap deve ser
registrado explicitamente em `GAP_REGISTER.yaml`, não escondido.

## O que este lema é, e por que é o único fragmento formalizável desta
   frente nesta rodada

A hipótese sob auditoria (Hessiana de pressão / alinhamento) depende, na
sua origem, de uma identidade algébrica elementar e totalmente rigorosa
que junta o Hessiano de pressão à decomposição `∇u = A + Ω` (parte
simétrica/taxa de deformação + parte antissimétrica/vorticidade):

    tr(A · Ω) = 0   para toda A simétrica, Ω antissimétrica.

Essa identidade é o primeiro passo, sem nenhuma parte heurística, da
equação de Poisson para a pressão (`-Δp = tr((∇u)²) = tr(A²) + tr(Ω²)`,
usada em `COMPUTATION/restricted_euler.py`) e da equação de Euler
restrita (Vieillefosse 1982). É pequena, autocontida, não depende de EDP
nem de Sobolev — só de álgebra linear finita — e por isso é o único
pedaço desta frente que está genuinamente ao alcance de uma formalização
nesta rodada. O resto da hipótese (sinal e taxa da parte anisotrópica e
não-local do Hessiano de pressão — "Lemma 3.1" no documento legado)
continua `NOT_FORMALIZED`: não é um lema de álgebra finita, é uma
estimativa não-local (tipo Biot–Savart) sobre soluções de Navier–Stokes,
e nenhuma auditoria de literatura substitui a prova que falta (ver
`REVIEWS/AUDIT_REPORT.md`).
-/

import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Basis
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NoncommRing

namespace TamesisNSPressureAudit

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Se `A` é simétrica (`Aᵀ = A`) e `Ω` é antissimétrica (`Ωᵀ = -Ω`),
então `tr(A * Ω) = 0`.

Esta é exatamente a identidade usada para decompor
`tr((∇u)²) = tr(A²) + tr(Ω²)` (o termo cruzado `tr(AΩ)` desaparece),
o primeiro passo, totalmente clássico, por trás da equação de Poisson
da pressão e da equação de Euler restrita. Verificada simbolicamente
para o caso 3×3 concreto com `sympy` em
`COMPUTATION/restricted_euler.py` (não é uma prova formal, é uma
checagem numérica/simbólica de caso finito que motivou este enunciado
geral). -/
theorem trace_symm_mul_skew_eq_zero
    (A Ω : Matrix n n ℝ) (hA : Aᵀ = A) (hΩ : Ωᵀ = -Ω) :
    (A * Ω).trace = 0 := by
  have h1 : (A * Ω).trace = ((A * Ω)ᵀ).trace := (Matrix.trace_transpose (A * Ω)).symm
  rw [Matrix.transpose_mul, hA, hΩ, Matrix.neg_mul, Matrix.trace_neg,
      Matrix.trace_mul_comm Ω A] at h1
  -- h1 : (A * Ω).trace = -(A * Ω).trace
  linarith

/-- Corolário imediato, na forma usada pela decomposição do gradiente de
velocidade `M = A + Ω`: o traço de `M²` só vê a parte simétrica e a
parte antissimétrica separadamente, nunca o termo cruzado. Isto é o
passo algébrico exato por trás de `-Δp = tr(A²) + tr(Ω²)` (equação de
Poisson da pressão) e de `dA/dt = -A² - Ω² + (1/3)tr(A²+Ω²) I` (Euler
restrita, Vieillefosse 1982) usadas em `COMPUTATION/restricted_euler.py`. -/
theorem trace_sq_decomposition
    (A Ω : Matrix n n ℝ) (hA : Aᵀ = A) (hΩ : Ωᵀ = -Ω) :
    ((A + Ω) * (A + Ω)).trace = (A * A).trace + (Ω * Ω).trace := by
  have expand : (A + Ω) * (A + Ω) = A * A + A * Ω + Ω * A + Ω * Ω := by
    noncomm_ring
  rw [expand, Matrix.trace_add, Matrix.trace_add, Matrix.trace_add]
  have hAΩ : (A * Ω).trace = 0 := trace_symm_mul_skew_eq_zero A Ω hA hΩ
  have hΩA : (Ω * A).trace = 0 := by
    have := trace_symm_mul_skew_eq_zero A Ω hA hΩ
    rw [Matrix.trace_mul_comm] at this
    exact this
  rw [hAΩ, hΩA]
  ring

end TamesisNSPressureAudit

/-
GAPS DELIBERADAMENTE NÃO ATACADOS NESTE RASCUNHO (registrados também em
GAP_REGISTER.yaml, não escondidos aqui):

1. A parte anisotrópica do Hessiano de pressão `H_p - (1/3)(tr H_p) I`
   não tem fórmula local fechada — é dada por uma integral singular
   (tipo Biot–Savart / Riesz) sobre todo o domínio. Nenhuma parte disso
   é uma identidade de álgebra linear finita; não está ao alcance de um
   lema autocontido como os acima.
2. A conexão entre `tr(A²)`, `tr(Ω²)` (aqui) e o cosseno de alinhamento
   `α₁ = cos²(ω, e₁)` do documento legado não foi formalizada — requer
   definir o autovetor de maior autovalor de `A` como função contínua
   (bem definida só onde os autovalores não colidem) e não foi tentada
   nesta rodada.
3. Nenhuma parte deste arquivo formaliza a equação de Navier–Stokes em
   si (nem fraca nem forte); os objetos aqui são puramente de álgebra
   linear finita (matrizes reais `n × n`), instanciados pontualmente em
   `∇u(x,t)` só na leitura matemática, não no Lean.
-/
