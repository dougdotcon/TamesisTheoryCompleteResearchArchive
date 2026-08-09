/-
FOUND-CF-DEPLETION-KERNEL-001 — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`PressureHessianAlgebra.lean` (mesma pasta): arquivo Lean autônomo,
verificado via `lake env lean` diretamente contra o mesmo projeto
Mathlib, fora da árvore de import compartilhada.

## O que este arquivo formaliza

Fonte primária: P. Constantin, C. Fefferman, "Direction of vorticity and
the problem of global regularity for the Navier-Stokes equations",
*Indiana Univ. Math. J.* 42 (1993), 775-789.

Equações restatadas com numeração em Siran Li, "On Vortex Alignment and
Boundedness of L^q Norm of Vorticity", *Acta Math. Sci.* 40(6) (2020),
arXiv:1712.00551, eq. 2.1-2.3 (citando Constantin 1994 para a
representação integral original):

```text
S(t,x) = (3/8π) p.v. ∫ { (x̂-y)⊗((x̂-y)×ω(t,x)) + ((x̂-y)×ω(t,x))⊗(x̂-y) }
           / |x-y|³  dy                                          (2.1)

S : (ω̂⊗ω̂)(t,x) = (3/4π) p.v. ∫ D(x̂-y, ω̂(t,x), ω̂(t,x-y)) |ω(t,x-y)|
                     / |x-y|³  dy                                 (2.2)

D(e1,e2,e3) := (e1·e3) · det(e1,e2,e3)                            (2.3)
```

`D` é um núcleo puramente algébrico de três vetores em ℝ³ — nenhuma
integral singular, nenhuma teoria de solução fraca é necessária para
estudá-lo isoladamente. É exatamente o mesmo tipo de "núcleo algébrico
dentro de uma estimativa maior" que `PressureHessianAlgebra.lean` já
tratou nesta sessão (`tr(AΩ)=0`).

Formalizamos aqui, e apenas aqui:

1. `D e1 e2 e2 = 0` — depleção EXATA quando as direções coincidem
   (o determinante com duas linhas iguais se anula; forma alternada).
2. Uma cota quantitativa `|D e1 e2 e3| ≤ ‖e2 - e3‖` para `‖e1‖,‖e2‖,‖e3‖
   ≤ 1` — conectando diretamente à hipótese de Lipschitz
   `|sin φ(t,x,y)| ≤ |x-y|/ρ` do teorema real (Li 2020, eq. 1.7/1.9):
   quando a direção da vorticidade varia pouco (`‖e2-e3‖` pequeno), o
   núcleo de estiramento `D` também é pequeno, mesmo antes de qualquer
   análise da integral.
3. Uma instância numérica concreta, não-vazia, exibindo o fenômeno de
   depleção: `D` pequeno quando `e2`, `e3` estão próximos.

Nenhuma prova incompleta nem premissa não justificada foi usada — se
algum passo abaixo não fechasse ao compilar de fato, o gap seria
registrado explicitamente em `GAP_REGISTER.yaml`, não escondido.
-/

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct
import Mathlib.LinearAlgebra.CrossProduct
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Tactic

namespace TamesisNSConstantinFeffermanDepletion

open Matrix InnerProductGeometry

/-- O produto triplo escalar `e1 · (e2 × e3)`, realizado em
`EuclideanSpace ℝ (Fin 3)` (o produto vetorial `⨯₃` de
`Mathlib.LinearAlgebra.CrossProduct` opera em `Fin 3 → ℝ`; `WithLp.ofLp`/
`WithLp.toLp` fazem a ponte com o tipo com norma L² usado para as cotas
de análise). Coincide com `Matrix.det ![e1,e2,e3]`, via
`triple_product_eq_det` de Mathlib -- não é usado diretamente aqui
porque `inner`/norma exigem o tipo `EuclideanSpace`, mas a igualdade
está registrada em `tripleProduct_eq_det` abaixo para documentar a
equivalência com a equação (2.3) na forma "det". -/
noncomputable def tripleProduct (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 (WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3))

/-- O núcleo de depleção de Constantin-Fefferman, equação (2.3) de Li
2020 (citando Constantin-Fefferman 1993):
`D(e1,e2,e3) := (e1·e3) · det(e1,e2,e3)`. -/
noncomputable def D (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 e3 * tripleProduct e1 e2 e3

/-- `tripleProduct` coincide com o determinante da matriz de linhas
`e1, e2, e3`, exatamente a leitura "det" da equação (2.3). -/
theorem tripleProduct_eq_det (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    tripleProduct e1 e2 e3
      = Matrix.det ![WithLp.ofLp e1, WithLp.ofLp e2, WithLp.ofLp e3] := by
  have hinner : inner ℝ e1 (WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3))
      = WithLp.ofLp e1 ⬝ᵥ (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3) := by
    rw [EuclideanSpace.inner_eq_star_dotProduct]
    simp [dotProduct_comm]
  rw [tripleProduct, hinner, triple_product_eq_det]

/-- **Depleção exata**: quando a segunda e a terceira direções
coincidem (`e2 = e3`), o produto triplo escalar se anula -- o
determinante com duas linhas iguais é zero. -/
@[simp] theorem tripleProduct_self_right (e1 e2 : EuclideanSpace ℝ (Fin 3)) :
    tripleProduct e1 e2 e2 = 0 := by
  simp [tripleProduct]

/-- **Depleção exata do núcleo `D`**: `D(e1,e2,e2) = 0`. Este é
exatamente o item 1 do escopo desta frente -- quando a direção da
vorticidade em `x` e em `x-y` coincide, o núcleo do estiramento
vorticial se anula identicamente, antes de qualquer estimativa
analítica. -/
theorem D_self_right (e1 e2 : EuclideanSpace ℝ (Fin 3)) :
    D e1 e2 e2 = 0 := by
  simp [D]

/-- Linearidade (na verdade, forma bilinear alternada) do produto
triplo no terceiro argumento: `tripleProduct e1 e2 e3` decompõe-se como
`tripleProduct e1 e2 (e3 - e2)` mais o termo já depletado
`tripleProduct e1 e2 e2 = 0`. -/
theorem tripleProduct_eq_sub (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    tripleProduct e1 e2 e3 = tripleProduct e1 e2 (e3 - e2) := by
  have key : tripleProduct e1 e2 (e3 - e2)
      = tripleProduct e1 e2 e3 - tripleProduct e1 e2 e2 := by
    simp only [tripleProduct, WithLp.ofLp_sub, map_sub, WithLp.toLp_sub, inner_sub_right]
  rw [key, tripleProduct_self_right, sub_zero]

/-- Cota do produto triplo: `|tripleProduct e1 e2 v| ≤ ‖e1‖ * ‖e2‖ *
‖v‖`, via Cauchy-Schwarz (`abs_real_inner_le_norm`) seguido da fórmula
do seno para a norma do produto vetorial
(`InnerProductGeometry.norm_ofLp_crossProduct`, Mathlib) e
`Real.sin_le_one`. -/
theorem abs_tripleProduct_le (e1 e2 v : EuclideanSpace ℝ (Fin 3)) :
    |tripleProduct e1 e2 v| ≤ ‖e1‖ * ‖e2‖ * ‖v‖ := by
  have hcs : |tripleProduct e1 e2 v|
      ≤ ‖e1‖ * ‖WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp v)‖ :=
    abs_real_inner_le_norm e1 _
  have hcross : ‖WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp v)‖
      = ‖e2‖ * ‖v‖ * Real.sin (InnerProductGeometry.angle e2 v) :=
    norm_ofLp_crossProduct e2 v
  have hsin : Real.sin (InnerProductGeometry.angle e2 v) ≤ 1 := Real.sin_le_one _
  have hnn : (0:ℝ) ≤ ‖e2‖ * ‖v‖ := by positivity
  calc |tripleProduct e1 e2 v|
      ≤ ‖e1‖ * ‖WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp v)‖ := hcs
    _ = ‖e1‖ * (‖e2‖ * ‖v‖ * Real.sin (InnerProductGeometry.angle e2 v)) := by
        rw [hcross]
    _ ≤ ‖e1‖ * (‖e2‖ * ‖v‖ * 1) := by
        gcongr
    _ = ‖e1‖ * ‖e2‖ * ‖v‖ := by ring

/-- **Cota quantitativa de depleção (item 2 do escopo)**: para vetores
`e1, e2, e3` com `‖e1‖, ‖e2‖, ‖e3‖ ≤ 1` (em particular vetores unitários,
o caso relevante para direções de vorticidade), o núcleo de
Constantin-Fefferman satisfaz `|D(e1,e2,e3)| ≤ ‖e2 - e3‖`. Esta é
exatamente a conexão geométrica com a hipótese de Lipschitz
`|sin φ(t,x,y)| ≤ |x-y|/ρ` do teorema real (Li 2020, eq. 1.7/1.9): quando
a direção da vorticidade varia pouco, o núcleo de estiramento também
varia pouco, com constante 1. -/
theorem abs_D_le (e1 e2 e3 : EuclideanSpace ℝ (Fin 3))
    (h1 : ‖e1‖ ≤ 1) (h2 : ‖e2‖ ≤ 1) (h3 : ‖e3‖ ≤ 1) :
    |D e1 e2 e3| ≤ ‖e2 - e3‖ := by
  have hne1 : (0:ℝ) ≤ ‖e1‖ := norm_nonneg _
  have hne3 : (0:ℝ) ≤ ‖e3‖ := norm_nonneg _
  have hstep1 : |D e1 e2 e3| = |inner ℝ e1 e3| * |tripleProduct e1 e2 e3| := by
    rw [D, abs_mul]
  have hstep2 : |tripleProduct e1 e2 e3| = |tripleProduct e1 e2 (e3 - e2)| := by
    rw [tripleProduct_eq_sub]
  have hstep3 : |tripleProduct e1 e2 (e3 - e2)| ≤ ‖e1‖ * ‖e2‖ * ‖e3 - e2‖ :=
    abs_tripleProduct_le e1 e2 (e3 - e2)
  have hinner_le : |inner ℝ e1 e3| ≤ ‖e1‖ * ‖e3‖ := abs_real_inner_le_norm e1 e3
  have hinner_nn : (0:ℝ) ≤ |inner ℝ e1 e3| := abs_nonneg _
  have hprod : |D e1 e2 e3| ≤ (‖e1‖ * ‖e3‖) * (‖e1‖ * ‖e2‖ * ‖e3 - e2‖) := by
    rw [hstep1, hstep2]
    exact mul_le_mul hinner_le hstep3 (abs_nonneg _) (by positivity)
  have hbound : (‖e1‖ * ‖e3‖) * (‖e1‖ * ‖e2‖ * ‖e3 - e2‖) ≤ 1 * (1 * 1 * ‖e3 - e2‖) := by
    have hnn2 : (0:ℝ) ≤ ‖e2‖ := norm_nonneg _
    have hnn3s : (0:ℝ) ≤ ‖e3 - e2‖ := norm_nonneg _
    have he13 : ‖e1‖ * ‖e3‖ ≤ 1 := by nlinarith
    gcongr
  have hfinal : |D e1 e2 e3| ≤ ‖e3 - e2‖ := by
    refine hprod.trans ?_
    simpa using hbound
  rw [norm_sub_rev] at hfinal
  exact hfinal

/-! ## Instância concreta positiva (item 3 do escopo)

`e1, e2, e3` são vetores unitários explícitos (parametrização racional
do círculo, `(3,4,5)` e `(7,24,25)`), com `e2, e3` próximos (ângulo
pequeno) e `e1` fora do plano de `e2, e3`, produzindo `D` estritamente
menor que a cota `‖e2-e3‖`, de modo não-vazio e não-trivial (`e1 ≠ e2`,
`e2 ≠ e3`). -/

noncomputable def e1Ex : EuclideanSpace ℝ (Fin 3) := !₂[(0:ℝ), 3/5, 4/5]
noncomputable def e2Ex : EuclideanSpace ℝ (Fin 3) := !₂[(1:ℝ), 0, 0]
noncomputable def e3Ex : EuclideanSpace ℝ (Fin 3) := !₂[(24:ℝ)/25, 7/25, 0]

theorem norm_e1Ex : ‖e1Ex‖ = 1 := by
  rw [e1Ex, EuclideanSpace.norm_eq]
  simp [Fin.sum_univ_three]
  norm_num

theorem norm_e2Ex : ‖e2Ex‖ = 1 := by
  rw [e2Ex, EuclideanSpace.norm_eq]
  simp [Fin.sum_univ_three]

theorem norm_e3Ex : ‖e3Ex‖ = 1 := by
  rw [e3Ex, EuclideanSpace.norm_eq]
  simp [Fin.sum_univ_three]
  norm_num

/-- Valor exato de `D` na instância concreta: `588/15625`, um número
pequeno e não-nulo. -/
theorem D_e1Ex_e2Ex_e3Ex : D e1Ex e2Ex e3Ex = 588 / 15625 := by
  rw [D, tripleProduct, e1Ex, e2Ex, e3Ex]
  simp [inner, Fin.sum_univ_three, cross_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  norm_num

/-- **Instância positiva não-vazia**: com os vetores unitários
explícitos acima, `e2Ex` e `e3Ex` estão próximos (`‖e2Ex - e3Ex‖ =
√2/5 ≈ 0.283`) e `D` é estritamente menor -- cerca de 13% da cota --
demonstrando numericamente o fenômeno de depleção: quando as direções
de vorticidade estão próximas, o núcleo de estiramento é pequeno, e a
cota geral `abs_D_le` de fato se verifica com folga neste caso
concreto. -/
theorem concrete_depletion_instance :
    D e1Ex e2Ex e3Ex ≤ ‖e2Ex - e3Ex‖ ∧ D e1Ex e2Ex e3Ex ≠ 0 := by
  constructor
  · have := abs_D_le e1Ex e2Ex e3Ex norm_e1Ex.le norm_e2Ex.le norm_e3Ex.le
    rw [D_e1Ex_e2Ex_e3Ex] at this ⊢
    exact (abs_le.mp this).2
  · rw [D_e1Ex_e2Ex_e3Ex]
    norm_num

end TamesisNSConstantinFeffermanDepletion

/-! ## O que NÃO é afirmado

```text
NÃO é uma prova do teorema de Constantin-Fefferman (1993)
NÃO prova nada sobre a representação integral p.v. (2.1)/(2.2) em si,
  nem sobre limitação de operadores integrais singulares
NÃO prova nenhuma cota de estiramento vorticial (vortex stretching) para
  soluções reais de Navier-Stokes
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO afirma que Navier-Stokes ficou alcançável
```

O que fica registrado como gap real e nomeado (já descrito em
`PORTFOLIO_REVIEW_CF_DEPLETION_KERNEL_2026_08_09.md`): a passagem de "D
é pequeno pontualmente" para "a integral p.v. de D contra o núcleo
1/|x-y|³ é controlada" é o passo de análise harmônica genuíno que falta
-- e é precisamente NS-GAP-001/004 na sua forma mais precisa. Este
arquivo NÃO fecha esse gap; formaliza apenas o núcleo algébrico puro,
citado precisamente de:

- P. Constantin, C. Fefferman, "Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations", Indiana Univ.
  Math. J. 42 (1993), 775-789.
- Siran Li, "On Vortex Alignment and Boundedness of L^q Norm of
  Vorticity", Acta Math. Sci. 40(6) (2020), 1700-1708, arXiv:1712.00551,
  eq. 2.1-2.3 (restatação numerada usada aqui).
-/

#print axioms TamesisNSConstantinFeffermanDepletion.tripleProduct_eq_det
#print axioms TamesisNSConstantinFeffermanDepletion.tripleProduct_self_right
#print axioms TamesisNSConstantinFeffermanDepletion.D_self_right
#print axioms TamesisNSConstantinFeffermanDepletion.tripleProduct_eq_sub
#print axioms TamesisNSConstantinFeffermanDepletion.abs_tripleProduct_le
#print axioms TamesisNSConstantinFeffermanDepletion.abs_D_le
#print axioms TamesisNSConstantinFeffermanDepletion.norm_e1Ex
#print axioms TamesisNSConstantinFeffermanDepletion.norm_e2Ex
#print axioms TamesisNSConstantinFeffermanDepletion.norm_e3Ex
#print axioms TamesisNSConstantinFeffermanDepletion.D_e1Ex_e2Ex_e3Ex
#print axioms TamesisNSConstantinFeffermanDepletion.concrete_depletion_instance
