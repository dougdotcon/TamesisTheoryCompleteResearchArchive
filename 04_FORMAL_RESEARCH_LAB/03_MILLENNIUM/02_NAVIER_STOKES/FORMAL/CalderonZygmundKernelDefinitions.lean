/-
FOUND-CZ-KERNEL-DEFINITIONS-001 — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`ConstantinFeffermanDepletionKernel.lean` e `PressureHessianAlgebra.lean`
(mesma pasta): arquivo Lean autônomo, verificado via `lake env lean`
diretamente contra o mesmo projeto Mathlib, fora da árvore de import
compartilhada. Autorização: `PORTFOLIO_REVIEW_CZ_KERNEL_DEFINITIONS_2026_08_09.md`
(`FOUND-CZ-KERNEL-DEFINITIONS-001_AUTHORIZED`, extensão nomeada de `DEC-076`).

## Achado empírico que delimita esta frente

Busca exaustiva anterior no Mathlib (`05_FORMAL/lean/.lake/packages/mathlib/Mathlib`)
confirmou **zero** arquivos para teoria de Calderón-Zygmund, integrais
singulares, espaços BMO, função maximal de Hardy-Littlewood, estimativas
de tipo-fraco, interpolação de Marcinkiewicz, ou integrais de valor
principal em qualquer forma. Esse fato é aceito aqui sem re-derivação.

Este arquivo formaliza apenas a **camada definicional** decidida na
revisão de portfólio citada acima:

```text
1. Integral de valor principal LOCAL em ℝ³: p.v. ∫_{B_R(x₀)} f :=
   lim_{ε→0+} ∫_{ε≤|y-x₀|<R} f(y) dy, quando o limite existe.
2. Classe estrutural de núcleo Calderón-Zygmund em ℝ³: homogêneo de
   grau -3, suave fora da origem, média zero sobre a esfera unitária.
3. Verificação de homogeneidade (e, na medida do possível, suavidade)
   da peça de coeficiente congelado do núcleo de Constantin-Fefferman:
   K(y) := D(ŷ, e2, e3)/‖y‖³ para e2, e3 fixos.
```

Nenhuma limitação L^p, nenhuma decomposição de Calderón-Zygmund, nenhuma
estimativa de tipo-fraco, nenhuma interpolação de Marcinkiewicz, e
nenhuma aplicação à integral p.v. real das equações (2.1)/(2.2) de
Constantin-Fefferman a um campo de vorticidade genuíno são tentadas
aqui. Ver o bloco final "O que NÃO é afirmado".

## Sobre a restatação de `D` (núcleo de Constantin-Fefferman)

Por ser um arquivo autônomo fora da árvore `05_FORMAL/lean/`, este
arquivo NÃO pode `import` `ConstantinFeffermanDepletionKernel.lean`
(não há `.olean` para ele em `LEAN_PATH` — foi apenas verificado
isoladamente, nunca compilado como alvo de biblioteca). A definição de
`D` abaixo é uma **restatação verbatim** — mesma definição, mesmas
chamadas de API do Mathlib (`inner`, `tripleProduct` via `WithLp.toLp 2
(WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3)`) — da equação (2.3) de Li 2020 /
`D` de `FOUND-CF-DEPLETION-KERNEL-001`, feita exclusivamente para
isolamento de arquivo autônomo. NÃO é uma nova alegação matemática nem
uma re-derivação a partir do zero: a álgebra subjacente é idêntica e já
foi verificada de forma independente naquele item de trabalho fechado.

## Sobre a busca de medida de esfera no Mathlib (item 2 do escopo)

Busca dirigida (não apenas confiada no achado anterior) confirmou que o
Mathlib TEM uma facilidade de integração sobre a esfera unitária em um
espaço normado de dimensão finita: `MeasureTheory.Measure.toSphere`, em
`Mathlib.MeasureTheory.Constructions.HaarToSphere` (Yury Kudryashov).
Dada uma medida de Haar aditiva `μ` em `E`, `μ.toSphere` é uma medida
genuína, rotação-invariante (por construção, via a mudança de
coordenadas polares generalizada do arquivo), MAS ela vive no SUBTIPO
`↥(Metric.sphere (0:E) 1)`, não em `E` restrito à esfera. Para obter uma
medida em `E` (necessária para escrever `∫ y in Metric.sphere 0 1, K y
∂σ` com `K : E → ℝ`, exatamente a forma pedida no escopo), este arquivo
empurra `volume.toSphere` ao longo da inclusão do subtipo via
`MeasureTheory.Measure.map`, produzindo `sphereSurfaceMeasure` abaixo —
uma medida genuína em `E`, suportada na esfera unitária. Isso é
suficiente para ESCREVER a condição de média zero honestamente com uma
medida concreta do Mathlib, mas a classe estrutural `CZKernelClass`
abaixo ainda é PARAMETRIZADA por uma medida `μ : Measure E` arbitrária
fornecida pelo chamador (em vez de fixar `sphereSurfaceMeasure` como
única escolha), porque provar as propriedades de invariância/normalização
de `sphereSurfaceMeasure` que tornariam essa escolha canônica está fora
do escopo desta frente (nenhuma dessas propriedades é usada ou provada
aqui). `sphereSurfaceMeasure` é oferecida como a instanciação natural
recomendada, documentada, mas não forçada.
-/

import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Geometry.Euclidean.Angle.Unoriented.CrossProduct
import Mathlib.LinearAlgebra.CrossProduct
import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Normed.Lp.MeasurableSpace
import Mathlib.MeasureTheory.Measure.Haar.OfBasis
import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.Tactic

namespace TamesisNSCalderonZygmundKernelDefs

open Matrix InnerProductGeometry MeasureTheory

/-! ## Restatação isolada de `D` (ver nota no cabeçalho do arquivo)

Cópia verbatim de `tripleProduct` e `D` de
`ConstantinFeffermanDepletionKernel.lean` (`FOUND-CF-DEPLETION-KERNEL-001`,
já verificado de forma independente), restatada aqui apenas por
isolamento de arquivo autônomo. -/

/-- O produto triplo escalar `e1 · (e2 × e3)`, realizado em
`EuclideanSpace ℝ (Fin 3)`. Restatação verbatim, ver nota acima. -/
noncomputable def tripleProduct (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 (WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3))

/-- O núcleo de depleção de Constantin-Fefferman, equação (2.3) de Li
2020: `D(e1,e2,e3) := (e1·e3) · det(e1,e2,e3)`. Restatação verbatim, ver
nota acima. -/
noncomputable def D (e1 e2 e3 : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  inner ℝ e1 e3 * tripleProduct e1 e2 e3

/-! ## Parte 1 — integral de valor principal LOCAL em ℝ³

`HasLocalPV f x0 R L` afirma que o limite, quando `ε → 0⁺`, da integral
de `f` sobre a coroa `{ε ≤ ‖y-x0‖} ∩ B_R(x0)` (formalizada aqui como
`Metric.closedBall x0 R \ Metric.closedBall x0 ε`) é `L`. Formulação
LOCAL (raio `R` finito) -- o comportamento no infinito depende de
decaimento de `f`, fora do escopo aqui (ver
`PORTFOLIO_REVIEW_CZ_KERNEL_DEFINITIONS_2026_08_09.md`). -/
def HasLocalPV (f : EuclideanSpace ℝ (Fin 3) → ℝ) (x0 : EuclideanSpace ℝ (Fin 3))
    (R L : ℝ) : Prop :=
  Filter.Tendsto
    (fun ε : ℝ => ∫ y in (Metric.closedBall x0 R \ Metric.closedBall x0 ε), f y)
    (nhdsWithin 0 (Set.Ioi 0)) (nhds L)

/-- Unicidade do valor de valor-principal, quando existe: `nhds` em `ℝ`
é `T2Space` e `nhdsWithin 0 (Set.Ioi 0)` é `NeBot` (ambos instâncias
padrão do Mathlib para `ℝ`), então `tendsto_nhds_unique` se aplica
diretamente. -/
theorem HasLocalPV.unique {f : EuclideanSpace ℝ (Fin 3) → ℝ}
    {x0 : EuclideanSpace ℝ (Fin 3)} {R L L' : ℝ}
    (h : HasLocalPV f x0 R L) (h' : HasLocalPV f x0 R L') : L = L' := by
  unfold HasLocalPV at h h'
  exact tendsto_nhds_unique h h'

/-- `localPV f x0 R` é o valor do limite de valor-principal quando ele
existe (escolhido via `Classical.choice`/`dite`), e `0` caso contrário
(valor de fallback arbitrário, nunca usado quando o limite de fato
existe -- ver `localPV_eq` abaixo). -/
noncomputable def localPV (f : EuclideanSpace ℝ (Fin 3) → ℝ) (x0 : EuclideanSpace ℝ (Fin 3))
    (R : ℝ) : ℝ :=
  open Classical in
  if h : ∃ L, HasLocalPV f x0 R L then h.choose else 0

/-- `localPV` de fato calcula o limite quando ele existe: se
`HasLocalPV f x0 R L`, então `localPV f x0 R = L`. Consequência direta
de `HasLocalPV.unique` aplicada ao valor escolhido pelo `dite`. -/
theorem localPV_eq {f : EuclideanSpace ℝ (Fin 3) → ℝ} {x0 : EuclideanSpace ℝ (Fin 3)}
    {R L : ℝ} (h : HasLocalPV f x0 R L) : localPV f x0 R = L := by
  have hex : ∃ L, HasLocalPV f x0 R L := ⟨L, h⟩
  unfold localPV
  rw [dif_pos hex]
  exact hex.choose_spec.unique h

/-! ### Instância positiva não-degenerada (regra de governança)

Toda hipótese/predicado introduzido precisa de uma instância concreta
não-vazia. A função identicamente nula tem valor-principal trivialmente
igual a `0` em qualquer bola e para qualquer centro: a integral da
função nula sobre QUALQUER conjunto (em particular cada coroa) é `0`
identicamente em `ε`, então o limite é `0` sem qualquer análise. -/

theorem hasLocalPV_zero (x0 : EuclideanSpace ℝ (Fin 3)) (R : ℝ) :
    HasLocalPV (fun _ : EuclideanSpace ℝ (Fin 3) => (0 : ℝ)) x0 R 0 := by
  have hzero : (fun ε : ℝ =>
      ∫ y in (Metric.closedBall x0 R \ Metric.closedBall x0 ε),
        (fun _ : EuclideanSpace ℝ (Fin 3) => (0 : ℝ)) y) = fun _ : ℝ => (0 : ℝ) := by
    funext ε
    simp
  unfold HasLocalPV
  rw [hzero]
  exact tendsto_const_nhds

/-- `localPV` da função nula é `0`, para todo centro e raio -- instância
concreta e não-vazia exigida pela regra de governança. -/
theorem localPV_zero (x0 : EuclideanSpace ℝ (Fin 3)) (R : ℝ) :
    localPV (fun _ : EuclideanSpace ℝ (Fin 3) => (0 : ℝ)) x0 R = 0 :=
  localPV_eq (hasLocalPV_zero x0 R)

/-! ## Parte 2 — classe estrutural de núcleo de Calderón-Zygmund em ℝ³

Ver a nota "Sobre a busca de medida de esfera no Mathlib" no cabeçalho
do arquivo para a justificativa de `μ` ser um parâmetro explícito em vez
de uma medida de superfície fixa. -/

/-- Medida de superfície induzida em `EuclideanSpace ℝ (Fin 3)`,
suportada na esfera unitária, obtida empurrando a medida genuína de
Kudryashov `MeasureTheory.Measure.volume.toSphere` (que vive no subtipo
`↥(Metric.sphere 0 1)`) ao longo da inclusão desse subtipo em `E`, via
`MeasureTheory.Measure.map`. É a instanciação concreta recomendada para
o parâmetro `μ` de `CZKernelClass` abaixo, mas não é imposta como única
escolha -- ver nota do cabeçalho. -/
noncomputable def sphereSurfaceMeasure :
    MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3)) :=
  MeasureTheory.Measure.map
    ((↑) : (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) →
      EuclideanSpace ℝ (Fin 3))
    (MeasureTheory.volume.toSphere)

/-- Classe estrutural de núcleo de Calderón-Zygmund em `ℝ³`, relativa a
uma medida `μ` fornecida explicitamente pelo chamador (ver nota do
cabeçalho sobre `sphereSurfaceMeasure` como instanciação recomendada).
Três condições, na ordem do escopo autorizado:

* `homogeneous`: homogeneidade de grau `-3`, enunciada sem expoente real
  negativo (`t^3 * K (t • y) = K y` em vez de `K (t•y) = K y / t^3`, para
  evitar `Real.rpow`/divisão desnecessária -- ambas as formas são
  equivalentes quando `t > 0`).
* `smooth_off_origin`: suavidade `C^∞` fora da origem, via `ContDiffAt`
  pontual (mais fácil de instanciar do que `ContDiffOn` num `K`
  concreto, e implica `ContDiffOn` na região `{y ≠ 0}` via
  `contDiffOn_of_forall_contDiffAt` caso seja necessário depois).
* `mean_zero`: condição de cancelamento (média zero) sobre a esfera
  unitária, relativa à medida `μ` fornecida. -/
structure CZKernelClass
    (μ : MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3)))
    (K : EuclideanSpace ℝ (Fin 3) → ℝ) : Prop where
  homogeneous : ∀ y : EuclideanSpace ℝ (Fin 3), y ≠ 0 →
    ∀ t : ℝ, 0 < t → t ^ 3 * K (t • y) = K y
  smooth_off_origin : ∀ y : EuclideanSpace ℝ (Fin 3), y ≠ 0 → ContDiffAt ℝ ⊤ K y
  mean_zero : ∫ y in Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1, K y ∂μ = 0

/-! ## Parte 3 — peça de coeficiente congelado do núcleo de
Constantin-Fefferman: `K(y) := D(ŷ, e2, e3)/‖y‖³`

Para `e2, e3` fixos ("coeficientes congelados" -- a direção de
vorticidade em `x` e o valor de `|ω(t,x-y)|` são tratados como
parâmetros fixos aqui, não como campos, exatamente como no escopo
autorizado). -/

/-- Projeção radial: `ŷ := y/‖y‖`. -/
noncomputable def yHat (y : EuclideanSpace ℝ (Fin 3)) : EuclideanSpace ℝ (Fin 3) :=
  ‖y‖⁻¹ • y

/-- A peça de coeficiente congelado do núcleo de Constantin-Fefferman:
`K(y) := D(ŷ, e2, e3)/‖y‖³`. -/
noncomputable def K (e2 e3 y : EuclideanSpace ℝ (Fin 3)) : ℝ :=
  D (yHat y) e2 e3 / ‖y‖ ^ 3

/-- **Fato genuinamente tratável (item central do escopo)**:
normalizar remove um fator escalar positivo -- `yHat` é invariante por
reescala positiva. Segue de `norm_smul`, `abs_of_pos`, e álgebra básica
de `smul`. -/
theorem yHat_smul_of_pos (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0)
    (t : ℝ) (ht : 0 < t) : yHat (t • y) = yHat y := by
  have hty : ‖t • y‖ = t * ‖y‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos ht]
  unfold yHat
  rw [hty, mul_inv, smul_smul]
  congr 1
  field_simp

/-- **Homogeneidade de grau `-3` de `K e2 e3` (item que este escopo NÃO
deveria comprometer)**: para `y ≠ 0` e `t > 0`,
`t^3 * K e2 e3 (t • y) = K e2 e3 y`. Consequência direta de
`yHat_smul_of_pos` e da homogeneidade explícita de `‖·‖³` sob reescala
positiva. -/
theorem K_homogeneous (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0) (t : ℝ) (ht : 0 < t) :
    t ^ 3 * K e2 e3 (t • y) = K e2 e3 y := by
  have hty : ‖t • y‖ = t * ‖y‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos ht]
  have hyhat : yHat (t • y) = yHat y := yHat_smul_of_pos y hy t ht
  have hynorm : ‖y‖ ≠ 0 := norm_ne_zero_iff.mpr hy
  have ht0 : t ≠ 0 := ht.ne'
  unfold K
  rw [hyhat, hty, mul_pow]
  field_simp

/-! ### Suavidade de `K e2 e3` fora da origem

Tentativa genuína (não exigida pelo escopo, mas tratável com a API de
`ContDiffAt` do Mathlib): `D(·, e2, e3)` é um produto de dois
funcionais lineares contínuos em `e1` (para `e2, e3` fixos), portanto
`C^∞` em TODO `E`; compondo com `yHat` (suave fora da origem) e dividindo
por `‖·‖³` (suave e não-nula fora da origem) dá suavidade de `K e2 e3`
fora da origem. -/

/-- `D(·, e2, e3)` é `C^∞` em toda a `EuclideanSpace ℝ (Fin 3)` (sem
excluir a origem): é o produto de dois funcionais lineares contínuos em
`e1`, `e1 ↦ ⟪e1,e3⟫` e `e1 ↦ ⟪e1, e2×e3⟫`. -/
theorem contDiff_D_fst (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ContDiff ℝ ⊤ (fun e1 : EuclideanSpace ℝ (Fin 3) => D e1 e2 e3) := by
  unfold D tripleProduct
  exact (contDiff_id.inner ℝ contDiff_const).mul (contDiff_id.inner ℝ contDiff_const)

/-- `yHat` é `C^∞` fora da origem: quociente `‖·‖⁻¹ • id`, com `‖·‖⁻¹`
suave e não-singular fora da origem (`contDiffAt_norm`, Mathlib) e `id`
suave em toda parte. -/
theorem contDiffAt_yHat (y : EuclideanSpace ℝ (Fin 3)) (hy : y ≠ 0) :
    ContDiffAt ℝ ⊤ yHat y := by
  unfold yHat
  have hnorm : ContDiffAt ℝ (⊤ : WithTop ℕ∞) (‖·‖ : EuclideanSpace ℝ (Fin 3) → ℝ) y :=
    contDiffAt_norm (𝕜 := ℝ) hy
  have hinv : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => ‖z‖⁻¹) y :=
    hnorm.inv (norm_ne_zero_iff.mpr hy)
  exact hinv.smul contDiffAt_id

/-- **`K e2 e3` é `C^∞` fora da origem**: composição de `D(·,e2,e3)`
(suave em toda parte) com `yHat` (suave fora da origem), dividida por
`‖·‖³` (suave e não-nula fora da origem). Instancia o campo
`smooth_off_origin` de `CZKernelClass` para o `K` concreto desta seção. -/
theorem contDiffAt_K (e2 e3 : EuclideanSpace ℝ (Fin 3)) {y : EuclideanSpace ℝ (Fin 3)}
    (hy : y ≠ 0) : ContDiffAt ℝ ⊤ (K e2 e3) y := by
  have hD : ContDiffAt ℝ (⊤ : WithTop ℕ∞) (fun e1 : EuclideanSpace ℝ (Fin 3) => D e1 e2 e3)
      (yHat y) := (contDiff_D_fst e2 e3).contDiffAt
  have hcomp : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => D (yHat z) e2 e3) y :=
    hD.comp y (contDiffAt_yHat y hy)
  have hnorm3 : ContDiffAt ℝ (⊤ : WithTop ℕ∞)
      (fun z : EuclideanSpace ℝ (Fin 3) => ‖z‖ ^ 3) y :=
    (contDiffAt_norm (𝕜 := ℝ) hy).pow 3
  have hne : ‖y‖ ^ 3 ≠ 0 := pow_ne_zero 3 (norm_ne_zero_iff.mpr hy)
  exact hcomp.div hnorm3 hne

end TamesisNSCalderonZygmundKernelDefs

/-! ## O que NÃO é afirmado

```text
NÃO prova nenhuma limitação L^p de operador integral singular
NÃO prova nenhum teorema de Calderón-Zygmund (decomposição, tipo-fraco,
  interpolação de Marcinkiewicz)
NÃO prova nada sobre a integral p.v. real das equações (2.1)/(2.2) de
  Constantin-Fefferman aplicada a um campo de vorticidade genuíno
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO afirma que Navier-Stokes ficou alcançável, aproximável, ou resolvido
```

## Item registrado como intratável nesta janela de escopo: `mean_zero`
para o `K e2 e3` concreto da Parte 3

Diferente da homogeneidade e da suavidade, a condição de média zero
`∫ y in Metric.sphere 0 1, K e2 e3 y ∂μ = 0` NÃO foi tentada para o `K`
concreto acima. Motivo preciso: essa condição exige calcular de fato uma
integral de superfície não-trivial de uma função racional em `D(ŷ,e2,e3)`
sobre a esfera unitária -- um cálculo analítico genuíno (não uma
identidade puramente algébrica, ao contrário da homogeneidade, e não uma
composição mecânica de suavidades, ao contrário de `contDiffAt_K`).
Nenhuma simetria de paridade óbvia de `D` (em relação a `e1 ↦ -e1`, por
exemplo) permite reduzir isso a uma manipulação algébrica curta: `D` não
é par nem ímpar em `e1` de forma exploitável sem análise adicional.
Consequentemente, NENHUM termo completo de `CZKernelClass μ (K e2 e3)`
é exibido neste arquivo para nenhuma medida `μ` -- apenas os dois campos
tratáveis (`homogeneous`, `smooth_off_origin`) são provados como teoremas
autônomos (`K_homogeneous`, `contDiffAt_K`). Isso é consistente com o
escopo autorizado em `PORTFOLIO_REVIEW_CZ_KERNEL_DEFINITIONS_2026_08_09.md`,
que pede a tentativa mas explicitamente permite não forçá-la.

Fontes citadas:
- P. Constantin, C. Fefferman, "Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations", Indiana Univ.
  Math. J. 42 (1993), 775-789.
- Siran Li, "On Vortex Alignment and Boundedness of L^q Norm of
  Vorticity", Acta Math. Sci. 40(6) (2020), 1700-1708, arXiv:1712.00551,
  eq. 2.1-2.3.
- `MeasureTheory.Measure.toSphere`, Yury Kudryashov,
  `Mathlib.MeasureTheory.Constructions.HaarToSphere`.
-/

#print axioms TamesisNSCalderonZygmundKernelDefs.tripleProduct
#print axioms TamesisNSCalderonZygmundKernelDefs.D
#print axioms TamesisNSCalderonZygmundKernelDefs.HasLocalPV.unique
#print axioms TamesisNSCalderonZygmundKernelDefs.localPV_eq
#print axioms TamesisNSCalderonZygmundKernelDefs.hasLocalPV_zero
#print axioms TamesisNSCalderonZygmundKernelDefs.localPV_zero
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.yHat_smul_of_pos
#print axioms TamesisNSCalderonZygmundKernelDefs.K_homogeneous
#print axioms TamesisNSCalderonZygmundKernelDefs.contDiff_D_fst
#print axioms TamesisNSCalderonZygmundKernelDefs.contDiffAt_yHat
#print axioms TamesisNSCalderonZygmundKernelDefs.contDiffAt_K
