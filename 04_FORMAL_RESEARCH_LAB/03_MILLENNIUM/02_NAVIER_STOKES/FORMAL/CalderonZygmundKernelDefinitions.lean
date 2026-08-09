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
import Mathlib.Analysis.Normed.Lp.PiLp
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.Tactic

namespace TamesisNSCalderonZygmundKernelDefs

open Matrix InnerProductGeometry MeasureTheory Set
open scoped Pointwise

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
  concreto). Se `ContDiffOn` na região `{y ≠ 0}` for necessário depois,
  segue por composição pontual de `ContDiffAt.contDiffWithinAt`
  (Mathlib) sobre cada `y` do conjunto -- não há um único lema "forall"
  pronto no Mathlib para essa passagem; é uma aplicação direta,
  não usada neste arquivo.
* `mean_zero`: condição de cancelamento (média zero) sobre a esfera
  unitária, relativa à medida `μ` fornecida.

Nota de honestidade (achado da revisão adversarial): esta classe é
PARAMETRIZADA por `μ` arbitrária, então `mean_zero` é trivialmente
satisfeita por QUALQUER `K` quando `μ` é a medida nula (ou qualquer
medida degenerada) -- `CZKernelClass 0 K` não tem conteúdo para nenhum
`K`. A instanciação com conteúdo real é `sphereSurfaceMeasure` (definida
acima), que é genuinamente não-nula e suportada na esfera. Nenhum termo
de `CZKernelClass` é construído neste arquivo para nenhuma medida --
ver a nota final "O que NÃO é afirmado". -/
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

/-! ## Parte 4 — fechamento de `mean_zero` para `K e2 e3` sobre
`sphereSurfaceMeasure`

Extensão autorizada por `PORTFOLIO_REVIEW_CZ_MEAN_ZERO_2026_08_09.md`
(`FOUND-CZ-MEAN-ZERO-001_AUTHORIZED`). Segue exatamente o argumento
verificado nessa revisão (citando Grafakos, *Classical Fourier
Analysis*, 3ª ed., §5.1.4/5.2.1-5.2.2): `D(θ,e2,e3) = (θ·e3)(θ·w)`,
`w := e2×e3`, é uma forma quadrática em `θ`; se o tensor de segundo
momento de `μ` é isotrópico (`∫ θᵢθⱼ dμ = c·δᵢⱼ`), então
`∫ D(θ,e2,e3) dμ = c·(e3·w) = c·tripleProduct e3 e2 e3 = 0` (produto
triplo com o primeiro e terceiro argumento iguais -- `dot_cross_self`).

Duas partes, na ordem do escopo autorizado:

* Parte A (`tripleProduct_self_left`, `IsotropicSecondMoment`,
  `integral_D_eq_zero_of_isotropicSecondMoment`): a redução puramente
  algébrica/de integração acima, condicional a uma hipótese de isotropia
  arbitrária -- não depende de `sphereSurfaceMeasure` nem de nenhuma
  maquinaria de invariância por rotação.
* Parte B (`sphereSurfaceMeasure_map_linearIsometryEquiv` e o que segue):
  estabelece que `sphereSurfaceMeasure` de fato tem essa propriedade de
  isotropia. A rota seguida seguiu exatamente a estratégia recomendada
  na revisão -- não a invariância pelo grupo `SO(3)` completo, mas pelo
  grupo finito gerado por permutações de coordenadas e inversões de
  sinal por coordenada, cada uma realizada como um
  `LinearIsometryEquiv ℝ E E` concreto (`flipCoord`, `permCoord`, via
  `LinearIsometryEquiv.piLpCongrRight`/`piLpCongrLeft`, Mathlib). A
  invariância de `sphereSurfaceMeasure` sob qualquer isometria linear de
  `E` é obtida a partir de `LinearIsometryEquiv.measurePreserving`
  (Mathlib, `Haar.InnerProductSpace`) aplicada à medida de Haar ambiente
  `volume`, propagada por `MeasureTheory.Measure.toSphere` via a fórmula
  `toSphere_apply'` (Kudryashov, `HaarToSphere.lean`) e a igualdade de
  conjuntos `(↑) '' (T'⁻¹' s) = T⁻¹' ((↑) '' s)` (imagem/pré-imagem sob a
  restrição de `T` à esfera), e então empurrada ao longo da inclusão do
  subtipo até `sphereSurfaceMeasure` em `E`. Isso fechou completamente a
  isotropia -- nenhum gap foi deixado nesta frente. -/

/-- **Parte A, passo algébrico**: `tripleProduct` com o primeiro e o
terceiro argumento iguais é zero -- `e3 · (e2 × e3) = 0`, ortogonalidade
padrão do produto vetorial ao seu segundo fator (`dot_cross_self`,
Mathlib `LinearAlgebra.CrossProduct`), reescrita na forma `inner`/`EuclideanSpace`
via `EuclideanSpace.inner_eq_star_dotProduct`. Distinto de
`tripleProduct_self_right`-style (não usado aqui, ver nota do cabeçalho
sobre o arquivo irmão `ConstantinFeffermanDepletionKernel.lean`): ali a
repetição é no 2º/3º argumento (via `cross_self`), aqui é no 1º/3º (via
`dot_cross_self`). -/
theorem tripleProduct_self_left (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    tripleProduct e3 e2 e3 = 0 := by
  unfold tripleProduct
  rw [EuclideanSpace.inner_eq_star_dotProduct]
  simp [dotProduct_comm, dot_cross_self]

/-- **Parte A, hipótese de isotropia**: `μ` tem tensor de segundo
momento isotrópico com constante `c` se, para cada par de coordenadas
`i,j : Fin 3`, `θ ↦ θ i * θ j` é `μ`-integrável e sua integral vale
`c` quando `i=j` e `0` caso contrário. Formulação com extração de
coordenada real via aplicação direta `θ i` (definitionalmente igual a
`WithLp.ofLp θ i` para `EuclideanSpace`, mesmo padrão usado em
`EuclideanSpace.norm_eq`/`Fin.sum_univ_three` já empregado no arquivo
irmão `ConstantinFeffermanDepletionKernel.lean`). -/
def IsotropicSecondMoment (μ : MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3))) (c : ℝ) : Prop :=
  (∀ i j : Fin 3, Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => θ i * θ j) μ) ∧
  (∀ i j : Fin 3, ∫ θ, θ i * θ j ∂μ = c * (if i = j then (1:ℝ) else 0))

/-- **Parte A, teorema principal (condicional)**: se `μ` tem tensor de
segundo momento isotrópico com constante `c`, então
`∫ D(θ,e2,e3) dμ = 0` para quaisquer `e2, e3` fixos. Prova: expande
`D(θ,e2,e3) = (θ·e3)(θ·w)` (`w := e2×e3`) como soma dupla explícita
`∑ i,j, (e3ᵢ wⱼ)(θᵢθⱼ)` sobre `Fin 3 × Fin 3` (nove termos), troca soma
por integral via `integral_finsetSum` (usando a integrabilidade de cada
termo, parte de `hiso`), aplica a hipótese de isotropia termo a termo
(colapsando os seis termos fora da diagonal para `0` e os três da
diagonal para `c`), obtendo `c * (e3·w) = c * tripleProduct e3 e2 e3`,
que é `0` por `tripleProduct_self_left`. Não depende de
`sphereSurfaceMeasure`: vale para qualquer `μ` que satisfaça a hipótese
de isotropia. -/
theorem integral_D_eq_zero_of_isotropicSecondMoment
    {μ : MeasureTheory.Measure (EuclideanSpace ℝ (Fin 3))} {c : ℝ}
    (hiso : IsotropicSecondMoment μ c) (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∫ θ, D θ e2 e3 ∂μ = 0 := by
  obtain ⟨hint, hval⟩ := hiso
  set w : EuclideanSpace ℝ (Fin 3) := WithLp.toLp 2 (WithLp.ofLp e2 ⨯₃ WithLp.ofLp e3) with hw
  have hDeq : ∀ θ : EuclideanSpace ℝ (Fin 3),
      D θ e2 e3 = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) := by
    intro θ
    unfold D tripleProduct
    rw [EuclideanSpace.inner_eq_star_dotProduct, EuclideanSpace.inner_eq_star_dotProduct]
    unfold dotProduct
    simp [Fin.sum_univ_three, Fintype.sum_prod_type]
    ring
  have hintg : ∀ p : Fin 3 × Fin 3,
      Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => (e3 p.1 * w p.2) * (θ p.1 * θ p.2)) μ :=
    fun p => (hint p.1 p.2).const_mul _
  calc ∫ θ, D θ e2 e3 ∂μ
      = ∫ θ, ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) ∂μ := by
        simp_rw [hDeq]
    _ = ∑ p : Fin 3 × Fin 3, ∫ θ, (e3 p.1 * w p.2) * (θ p.1 * θ p.2) ∂μ :=
        integral_finsetSum Finset.univ (fun p _ => hintg p)
    _ = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * ∫ θ, θ p.1 * θ p.2 ∂μ := by
        simp_rw [integral_const_mul]
    _ = ∑ p : Fin 3 × Fin 3, (e3 p.1 * w p.2) * (c * (if p.1 = p.2 then (1:ℝ) else 0)) := by
        simp_rw [hval]
    _ = c * ∑ i : Fin 3, e3 i * w i := by
        simp [Fintype.sum_prod_type, Fin.sum_univ_three]
        ring
    _ = c * tripleProduct e3 e2 e3 := by
        congr 1
        unfold tripleProduct
        rw [EuclideanSpace.inner_eq_star_dotProduct]
        unfold dotProduct
        simp [Fin.sum_univ_three]
        ring
    _ = 0 := by rw [tripleProduct_self_left]; ring

/-! ### Parte B — isotropia de `sphereSurfaceMeasure`

Estabelecida via invariância de `sphereSurfaceMeasure` sob QUALQUER
isometria linear de `E` (não apenas o grupo finito discutido no escopo
autorizado -- o argumento abaixo prova o caso geral diretamente, e o
grupo finito de permutações/inversões de sinal é aplicado como caso
particular). -/

/-- Volume (medida de Haar ambiente `volume` de `E`) da imagem de
QUALQUER conjunto sob uma isometria linear `T` é igual ao volume do
conjunto original -- sem hipótese de mensurabilidade em `B`, via
`MeasurableEquiv.map_apply` (válido para todo conjunto, não só
mensurável) aplicado a `T.toMeasurableEquiv`, usando
`LinearIsometryEquiv.measurePreserving` (Mathlib,
`Haar.InnerProductSpace`). -/
theorem volume_image_linearIsometryEquiv (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (B : Set (EuclideanSpace ℝ (Fin 3))) :
    (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) (T '' B) = MeasureTheory.volume B := by
  have hmp : Measure.map (⇑T) (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) =
      MeasureTheory.volume := (LinearIsometryEquiv.measurePreserving T).map_eq
  have h1 : Measure.map (⇑T.toMeasurableEquiv)
      (MeasureTheory.volume : Measure (EuclideanSpace ℝ (Fin 3))) (T '' B) = MeasureTheory.volume (T '' B) := by
    rw [LinearIsometryEquiv.coe_toMeasurableEquiv, hmp]
  rw [MeasurableEquiv.map_apply] at h1
  rw [LinearIsometryEquiv.coe_toMeasurableEquiv, Set.preimage_image_eq B T.injective] at h1
  exact h1.symm

/-- O cone `Ioo 0 1 • A` sobre `A` comuta com a imagem por uma isometria
linear `T`: `T '' (Ioo 0 1 • A) = Ioo 0 1 • (T '' A)`. Via
`iUnion_smul_set` (o cone é a união dos raios `t • A`) e `image_smul_set`
(um mapa linear comuta com a multiplicação por escalar em conjuntos). -/
theorem image_smul_Ioo_linearIsometryEquiv
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) (A : Set (EuclideanSpace ℝ (Fin 3))) :
    T '' (Set.Ioo (0:ℝ) 1 • A) = Set.Ioo (0:ℝ) 1 • (T '' A) := by
  rw [← iUnion_smul_set, ← iUnion_smul_set, Set.image_iUnion₂]
  simp_rw [image_smul_set (F := EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) T]

/-- Toda isometria linear de `E` mapeia a esfera unitária nela mesma
(preserva a norma). -/
theorem mapsTo_sphere (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Set.MapsTo T (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := by
  intro x hx
  simp only [Metric.mem_sphere, dist_zero_right] at hx ⊢
  rw [LinearIsometryEquiv.norm_map]
  exact hx

/-- Restrição de `T` à esfera unitária, como auto-mapa do subtipo
`↥(sphere 0 1)`, via `Set.MapsTo.restrict`. -/
noncomputable def sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) → (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) :=
  (mapsTo_sphere T).restrict T _ _

theorem sphereMap_continuous (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Continuous (sphereMap T) :=
  Continuous.subtype_mk (T.continuous.comp continuous_subtype_val) _

theorem sphereMap_measurable (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measurable (sphereMap T) := (sphereMap_continuous T).measurable

/-- Igualdade de conjuntos chave: a imagem pela inclusão do subtipo da
pré-imagem de `s` por `sphereMap T` é igual à pré-imagem por `T`
(em `E`) da imagem de `s` pela inclusão. Usa que `T` leva pontos fora
da esfera para fora da esfera (isometria) para garantir que ambos os
lados coincidem exatamente (não apenas na esfera). -/
theorem image_val_preimage_sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (s : Set (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1)) :
    ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) '' ((sphereMap T) ⁻¹' s)
      = T ⁻¹' (((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) '' s) := by
  ext y
  constructor
  · rintro ⟨x, hx, rfl⟩
    refine ⟨sphereMap T x, hx, ?_⟩
    show ((sphereMap T x : EuclideanSpace ℝ (Fin 3))) = T (x : EuclideanSpace ℝ (Fin 3))
    exact (Set.MapsTo.val_restrict_apply (mapsTo_sphere T) x)
  · rintro hy
    rw [Set.mem_preimage] at hy
    obtain ⟨x', hx', hx'eq⟩ := hy
    have hyS : y ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 := by
      have hx'2 : ‖(x' : EuclideanSpace ℝ (Fin 3))‖ = 1 := by
        have hx'3 := x'.2
        simp only [Metric.mem_sphere, dist_zero_right] at hx'3
        exact hx'3
      have hty : ‖T y‖ = 1 := by rw [← hx'eq]; exact hx'2
      simpa [Metric.mem_sphere, dist_zero_right, LinearIsometryEquiv.norm_map] using hty
    refine ⟨⟨y, hyS⟩, ?_, rfl⟩
    show sphereMap T ⟨y, hyS⟩ ∈ s
    have hval : ((sphereMap T ⟨y, hyS⟩ : EuclideanSpace ℝ (Fin 3))) = T y :=
      Set.MapsTo.val_restrict_apply (mapsTo_sphere T) ⟨y, hyS⟩
    have heq : sphereMap T ⟨y, hyS⟩ = x' := by
      apply Subtype.ext
      rw [hval, hx'eq]
    rwa [heq]

theorem preimage_eq_image_symm (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3))
    (A : Set (EuclideanSpace ℝ (Fin 3))) : T ⁻¹' A = T.symm '' A := by
  ext y
  simp only [Set.mem_preimage, Set.mem_image]
  constructor
  · intro h; exact ⟨T y, h, T.symm_apply_apply y⟩
  · rintro ⟨a, ha, rfl⟩; simpa using ha

/-- **Lema-chave da Parte B**: `volume.toSphere` (a medida genuína de
Kudryashov na esfera) é invariante sob a restrição `sphereMap T` de
qualquer isometria linear `T`. Combina `toSphere_apply'` (Kudryashov,
fórmula do cone) com `image_val_preimage_sphereMap`,
`preimage_eq_image_symm`, `image_smul_Ioo_linearIsometryEquiv` e
`volume_image_linearIsometryEquiv` acima. -/
theorem toSphere_map_sphereMap (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measure.map (sphereMap T) (MeasureTheory.volume.toSphere) = MeasureTheory.volume.toSphere := by
  apply Measure.ext
  intro s hs
  rw [Measure.map_apply (sphereMap_measurable T) hs]
  rw [Measure.toSphere_apply' _ hs, Measure.toSphere_apply' _ (hs.preimage (sphereMap_measurable T))]
  rw [image_val_preimage_sphereMap T s, preimage_eq_image_symm T]
  rw [← image_smul_Ioo_linearIsometryEquiv T.symm]
  rw [volume_image_linearIsometryEquiv T.symm]

/-- **Invariância de `sphereSurfaceMeasure` sob toda isometria linear de
`E`**: consequência de `toSphere_map_sphereMap`, propagada ao longo da
inclusão do subtipo via `Measure.map_map` (duas vezes) e a comutação
`(↑) ∘ sphereMap T = T ∘ (↑)` (`Set.MapsTo.restrict_commutes`,
Mathlib). Este é o fato central da Parte B: NÃO ficou como gap. -/
theorem sphereSurfaceMeasure_map_linearIsometryEquiv
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) :
    Measure.map T sphereSurfaceMeasure = sphereSurfaceMeasure := by
  unfold sphereSurfaceMeasure
  rw [Measure.map_map T.continuous.measurable measurable_subtype_coe]
  have hcomm : (T : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3)) ∘
        ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3))
      = ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) ∘ (sphereMap T) :=
    (Set.MapsTo.restrict_commutes T _ _ (mapsTo_sphere T)).symm
  rw [hcomm, ← Measure.map_map measurable_subtype_coe (sphereMap_measurable T),
    toSphere_map_sphereMap]

/-- `sphereSurfaceMeasure` dá massa total a.e. à esfera unitária:
`{θ | θ ∉ sphere 0 1}` tem pré-imagem vazia pela inclusão do subtipo. -/
theorem ae_mem_sphere_sphereSurfaceMeasure :
    ∀ᵐ θ ∂sphereSurfaceMeasure, θ ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 := by
  rw [ae_iff]
  have hmeas : MeasurableSet {x : EuclideanSpace ℝ (Fin 3) | ¬ x ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1} :=
    (Metric.isClosed_sphere).measurableSet.compl
  unfold sphereSurfaceMeasure
  rw [Measure.map_apply measurable_subtype_coe hmeas]
  have hempty : ((↑) : Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1 → EuclideanSpace ℝ (Fin 3)) ⁻¹'
      {x : EuclideanSpace ℝ (Fin 3) | ¬ x ∈ Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1} = ∅ := by
    ext x; simp
  rw [hempty]; simp

/-- `sphereSurfaceMeasure` é uma medida finita: pushforward, via
`Measure.map`, da medida `volume.toSphere` de Kudryashov, que já é
`IsFiniteMeasure` por instância do Mathlib
(`Measure.toSphere.instIsFiniteMeasure`, `HaarToSphere.lean`) --
pushforward de medida finita é finita. Necessária para a
integrabilidade abaixo (`integrable_const` requer medida finita). -/
instance instIsFiniteMeasure_sphereSurfaceMeasure : IsFiniteMeasure sphereSurfaceMeasure := by
  unfold sphereSurfaceMeasure
  infer_instance

/-- `θᵢθⱼ` é `sphereSurfaceMeasure`-integrável: limitada por `1` a.e.
(`|θᵢ| ≤ ‖θ‖ = 1` a.e., via `PiLp.norm_apply_le` e
`ae_mem_sphere_sphereSurfaceMeasure`), e `sphereSurfaceMeasure` é uma
medida finita (`instIsFiniteMeasure_sphereSurfaceMeasure` acima). -/
theorem integrable_coord_mul_sphereSurfaceMeasure (i j : Fin 3) :
    Integrable (fun θ : EuclideanSpace ℝ (Fin 3) => θ i * θ j) sphereSurfaceMeasure := by
  apply Integrable.mono' (integrable_const (1:ℝ))
  · fun_prop
  · filter_upwards [ae_mem_sphere_sphereSurfaceMeasure] with θ hθ
    have hθ' : ‖θ‖ = 1 := by simpa [Metric.mem_sphere, dist_zero_right] using hθ
    have hi : ‖θ i‖ ≤ 1 := by rw [← hθ']; exact PiLp.norm_apply_le θ i
    have hj : ‖θ j‖ ≤ 1 := by rw [← hθ']; exact PiLp.norm_apply_le θ j
    calc ‖θ i * θ j‖ = ‖θ i‖ * ‖θ j‖ := norm_mul _ _
      _ ≤ 1 * 1 := mul_le_mul hi hj (norm_nonneg _) (by norm_num)
      _ = 1 := by ring

/-- Inversão de sinal na coordenada `k` (mantendo as demais fixas), como
`LinearIsometryEquiv` de `E`: produto de isometrias unidimensionais de
`ℝ` (`LinearIsometryEquiv.neg`/`.refl`), via
`LinearIsometryEquiv.piLpCongrRight` (Mathlib, `Normed.Lp.PiLp`). -/
noncomputable def flipCoord (k : Fin 3) :
    EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3) :=
  LinearIsometryEquiv.piLpCongrRight 2
    (fun i => if i = k then LinearIsometryEquiv.neg ℝ else LinearIsometryEquiv.refl ℝ ℝ)

theorem flipCoord_apply_self (k : Fin 3) (θ : EuclideanSpace ℝ (Fin 3)) :
    (flipCoord k θ) k = - θ k := by
  unfold flipCoord
  rw [LinearIsometryEquiv.piLpCongrRight_apply]
  simp

theorem flipCoord_apply_other (k i : Fin 3) (θ : EuclideanSpace ℝ (Fin 3)) (h : i ≠ k) :
    (flipCoord k θ) i = θ i := by
  unfold flipCoord
  rw [LinearIsometryEquiv.piLpCongrRight_apply]
  simp [h]

/-- Permutação de coordenadas por `σ : Equiv.Perm (Fin 3)`, como
`LinearIsometryEquiv` de `E`, via `LinearIsometryEquiv.piLpCongrLeft`
(Mathlib, `Normed.Lp.PiLp`). -/
noncomputable def permCoord (σ : Equiv.Perm (Fin 3)) :
    EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3) :=
  LinearIsometryEquiv.piLpCongrLeft 2 ℝ ℝ σ

theorem permCoord_apply (σ : Equiv.Perm (Fin 3)) (θ : EuclideanSpace ℝ (Fin 3)) (i : Fin 3) :
    (permCoord σ θ) i = θ (σ.symm i) := by
  unfold permCoord
  rw [LinearIsometryEquiv.piLpCongrLeft_apply]
  simp [Equiv.piCongrLeft']

/-- Troca de integral por qualquer isometria linear de `E`, aplicada à
medida `sphereSurfaceMeasure` invariante: consequência direta de
`sphereSurfaceMeasure_map_linearIsometryEquiv` empacotada como
`MeasurePreserving` e `MeasurePreserving.integral_comp'` (Mathlib). -/
theorem integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
    (T : EuclideanSpace ℝ (Fin 3) ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin 3)) (g : EuclideanSpace ℝ (Fin 3) → ℝ) :
    ∫ θ, g (T θ) ∂sphereSurfaceMeasure = ∫ θ, g θ ∂sphereSurfaceMeasure := by
  have hMP : MeasurePreserving T.toMeasurableEquiv sphereSurfaceMeasure sphereSurfaceMeasure := by
    refine ⟨T.toMeasurableEquiv.measurable, ?_⟩
    rw [LinearIsometryEquiv.coe_toMeasurableEquiv]
    exact sphereSurfaceMeasure_map_linearIsometryEquiv T
  have hcomp := hMP.integral_comp' g
  simpa [LinearIsometryEquiv.coe_toMeasurableEquiv] using hcomp

/-- Termos fora da diagonal do tensor de segundo momento de
`sphereSurfaceMeasure` são zero: aplica-se `flipCoord i` (que troca o
sinal de `θᵢ` e mantém `θⱼ`, `j≠i`, fixo), obtendo
`∫θᵢθⱼ = ∫(-θᵢ)θⱼ = -∫θᵢθⱼ`, logo `∫θᵢθⱼ=0`. -/
theorem integral_offdiag_eq_zero_sphereSurfaceMeasure (i j : Fin 3) (h : i ≠ j) :
    ∫ θ, θ i * θ j ∂sphereSurfaceMeasure = 0 := by
  have hkey := integral_comp_linearIsometryEquiv_sphereSurfaceMeasure (flipCoord i)
    (fun θ => θ i * θ j)
  have hpt : ∀ θ : EuclideanSpace ℝ (Fin 3),
      (flipCoord i θ) i * (flipCoord i θ) j = - (θ i * θ j) := by
    intro θ
    rw [flipCoord_apply_self, flipCoord_apply_other i j θ (Ne.symm h)]
    ring
  simp_rw [hpt] at hkey
  rw [integral_neg] at hkey
  linarith

/-- Termos da diagonal do tensor de segundo momento de
`sphereSurfaceMeasure` coincidem entre si: aplica-se `permCoord` da
transposição `(i j)`, que troca `θᵢ` e `θⱼ`, obtendo
`∫θᵢθᵢ = ∫θⱼθⱼ`. -/
theorem integral_diag_eq_sphereSurfaceMeasure (i j : Fin 3) :
    ∫ θ, θ i * θ i ∂sphereSurfaceMeasure = ∫ θ, θ j * θ j ∂sphereSurfaceMeasure := by
  have hkey := integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
    (permCoord (Equiv.swap i j)) (fun θ => θ i * θ i)
  have hpt : ∀ θ : EuclideanSpace ℝ (Fin 3),
      (permCoord (Equiv.swap i j) θ) i * (permCoord (Equiv.swap i j) θ) i = θ j * θ j := by
    intro θ
    rw [permCoord_apply]
    simp [Equiv.symm_swap, Equiv.swap_apply_left]
  simp_rw [hpt] at hkey
  linarith

/-- **Fechamento da Parte B**: `sphereSurfaceMeasure` tem tensor de
segundo momento isotrópico, com constante `c := ∫θ₀² dμ` (escolha
concreta, canônica dado `Fin 3`). Combina
`integral_offdiag_eq_zero_sphereSurfaceMeasure` (fora da diagonal),
`integral_diag_eq_sphereSurfaceMeasure` (diagonal) e
`integrable_coord_mul_sphereSurfaceMeasure` (integrabilidade). -/
theorem sphereSurfaceMeasure_isotropicSecondMoment :
    IsotropicSecondMoment sphereSurfaceMeasure (∫ θ, θ 0 * θ 0 ∂sphereSurfaceMeasure) := by
  refine ⟨integrable_coord_mul_sphereSurfaceMeasure, ?_⟩
  intro i j
  by_cases h : i = j
  · subst h
    simp only [mul_one, ite_true]
    exact integral_diag_eq_sphereSurfaceMeasure i 0
  · simp only [if_neg h, mul_zero]
    exact integral_offdiag_eq_zero_sphereSurfaceMeasure i j h

/-- **`mean_zero` para `K e2 e3` sobre `sphereSurfaceMeasure`**: sobre a
esfera, `yHat y = y` e `‖y‖³=1`, logo `K e2 e3 y = D y e2 e3`; a integral
de conjunto sobre `sphere 0 1` coincide com a integral plena porque
`sphereSurfaceMeasure` já dá massa total a.e. à esfera
(`ae_mem_sphere_sphereSurfaceMeasure`, via `Measure.restrict_eq_self_of_ae_mem`);
o resultado segue de `integral_D_eq_zero_of_isotropicSecondMoment`
aplicado a `sphereSurfaceMeasure_isotropicSecondMoment`. Instancia o
campo `mean_zero` de `CZKernelClass` -- o item central desta frente. -/
theorem K_mean_zero_sphereSurfaceMeasure (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    ∫ y in Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1, K e2 e3 y ∂sphereSurfaceMeasure = 0 := by
  have heq : Set.EqOn (K e2 e3) (fun y => D y e2 e3) (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1) := by
    intro y hy
    have hynorm : ‖y‖ = 1 := by simpa [Metric.mem_sphere, dist_zero_right] using hy
    show D (yHat y) e2 e3 / ‖y‖ ^ 3 = D y e2 e3
    unfold yHat
    rw [hynorm]
    simp
  rw [setIntegral_congr_fun Metric.isClosed_sphere.measurableSet heq]
  show ∫ y, D y e2 e3 ∂(sphereSurfaceMeasure.restrict (Metric.sphere (0 : EuclideanSpace ℝ (Fin 3)) 1)) = 0
  rw [Measure.restrict_eq_self_of_ae_mem ae_mem_sphere_sphereSurfaceMeasure]
  exact integral_D_eq_zero_of_isotropicSecondMoment sphereSurfaceMeasure_isotropicSecondMoment e2 e3

/-- **Termo completo de `CZKernelClass`** para o núcleo de coeficiente
congelado de Constantin-Fefferman, relativo a `sphereSurfaceMeasure`,
para quaisquer `e2, e3` fixos: o primeiro termo completo desta classe em
todo o laboratório. Combina os três campos já provados:
`K_homogeneous` (homogeneidade, `FOUND-CZ-KERNEL-DEFINITIONS-001`),
`contDiffAt_K` (suavidade fora da origem, idem) e
`K_mean_zero_sphereSurfaceMeasure` (média zero, esta frente,
`FOUND-CZ-MEAN-ZERO-001`). -/
theorem czKernelClass_sphereSurfaceMeasure_K (e2 e3 : EuclideanSpace ℝ (Fin 3)) :
    CZKernelClass sphereSurfaceMeasure (K e2 e3) where
  homogeneous := K_homogeneous e2 e3
  smooth_off_origin := fun _ hy => contDiffAt_K e2 e3 hy
  mean_zero := K_mean_zero_sphereSurfaceMeasure e2 e3

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

## `mean_zero` fechado (atualização de `PORTFOLIO_REVIEW_CZ_MEAN_ZERO_2026_08_09.md`)

A nota anterior deste bloco registrava `mean_zero` como item intratável
nesta janela de escopo, supondo que exigisse um cálculo analítico de
integral de superfície genuíno. Uma revisão de portfólio posterior
(`PORTFOLIO_REVIEW_CZ_MEAN_ZERO_2026_08_09.md`,
`FOUND-CZ-MEAN-ZERO-001_AUTHORIZED`, citando Grafakos, *Classical
Fourier Analysis*, 3ª ed., Springer GTM 249, 2014, §5.1.4/§5.2.1-5.2.2)
identificou que essa suposição estava incorreta: `D(θ,e2,e3)` é uma
forma quadrática em `θ`, e sua média sobre a esfera se reduz a uma
identidade puramente algébrica (isotropia do tensor de segundo momento
mais `det`/`tripleProduct` com argumento repetido = 0), NÃO a um cálculo
analítico. Essa formalização está completa na Parte 4 acima:

* Parte A (`integral_D_eq_zero_of_isotropicSecondMoment`): a redução
  algébrica condicional, provada sem nenhuma hipótese sobre
  `sphereSurfaceMeasure` especificamente.
* Parte B (`sphereSurfaceMeasure_map_linearIsometryEquiv` e o que segue
  até `sphereSurfaceMeasure_isotropicSecondMoment`): a isotropia de
  `sphereSurfaceMeasure` foi estabelecida via invariância sob QUALQUER
  isometria linear de `E` -- não ficou como gap, nem precisou ser
  restrita ao subgrupo finito de permutações/inversões de sinal
  sugerido como estratégia de recuo no escopo autorizado (esse subgrupo
  finito é usado, mas apenas porque é suficiente, não porque a
  invariância geral tenha sido inalcançável).
* `K_mean_zero_sphereSurfaceMeasure` combina as duas partes e instancia
  literalmente o campo `mean_zero` de `CZKernelClass` para `K e2 e3` e
  `sphereSurfaceMeasure`.
* `czKernelClass_sphereSurfaceMeasure_K` é o termo completo resultante
  de `CZKernelClass sphereSurfaceMeasure (K e2 e3)`, para quaisquer
  `e2, e3` fixos -- o primeiro termo completo desta classe em todo o
  laboratório, combinando `K_homogeneous`, `contDiffAt_K` (ambos de
  `FOUND-CZ-KERNEL-DEFINITIONS-001`) e `K_mean_zero_sphereSurfaceMeasure`
  (desta frente).

Isso NÃO prova limitação L² do operador (exigiria a maquinaria completa
de Grafakos Prop. 5.2.3/Cor. 5.2.6 -- derivar um multiplicador de
Fourier a partir do núcleo espacial p.v., fora de escopo aqui), NÃO toca
o operador não-linear real das eq. 2.1/2.2 (onde `e3=ω̂(t,x-y)` varia com
`y`), e NÃO é progresso em NS-GAP-001/004. Ver também o bloco "O que NÃO
é afirmado" acima, que permanece válido sem alteração.

Fontes citadas:
- P. Constantin, C. Fefferman, "Direction of vorticity and the problem
  of global regularity for the Navier-Stokes equations", Indiana Univ.
  Math. J. 42 (1993), 775-789.
- Siran Li, "On Vortex Alignment and Boundedness of L^q Norm of
  Vorticity", Acta Math. Sci. 40(6) (2020), 1700-1708, arXiv:1712.00551,
  eq. 2.1-2.3.
- Loukas Grafakos, *Classical Fourier Analysis*, 3ª ed., Springer GTM
  249, 2014, §5.1.4 e §5.2.1-5.2.2 (achado que motivou esta frente --
  não usado diretamente na formalização, que é auto-contida em termos
  de álgebra linear + invariância de medida).
- `MeasureTheory.Measure.toSphere`, Yury Kudryashov,
  `Mathlib.MeasureTheory.Constructions.HaarToSphere`.
- `LinearIsometryEquiv.measurePreserving`, Sébastien Gouëzel,
  `Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace`.
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

-- Parte 4 (mean_zero) -- novas declarações
#print axioms TamesisNSCalderonZygmundKernelDefs.tripleProduct_self_left
#print axioms TamesisNSCalderonZygmundKernelDefs.integral_D_eq_zero_of_isotropicSecondMoment
#print axioms TamesisNSCalderonZygmundKernelDefs.volume_image_linearIsometryEquiv
#print axioms TamesisNSCalderonZygmundKernelDefs.image_smul_Ioo_linearIsometryEquiv
#print axioms TamesisNSCalderonZygmundKernelDefs.mapsTo_sphere
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereMap
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereMap_continuous
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereMap_measurable
#print axioms TamesisNSCalderonZygmundKernelDefs.image_val_preimage_sphereMap
#print axioms TamesisNSCalderonZygmundKernelDefs.preimage_eq_image_symm
#print axioms TamesisNSCalderonZygmundKernelDefs.toSphere_map_sphereMap
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereSurfaceMeasure_map_linearIsometryEquiv
#print axioms TamesisNSCalderonZygmundKernelDefs.ae_mem_sphere_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.instIsFiniteMeasure_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.integrable_coord_mul_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.flipCoord
#print axioms TamesisNSCalderonZygmundKernelDefs.flipCoord_apply_self
#print axioms TamesisNSCalderonZygmundKernelDefs.flipCoord_apply_other
#print axioms TamesisNSCalderonZygmundKernelDefs.permCoord
#print axioms TamesisNSCalderonZygmundKernelDefs.permCoord_apply
#print axioms TamesisNSCalderonZygmundKernelDefs.integral_comp_linearIsometryEquiv_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.integral_offdiag_eq_zero_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.integral_diag_eq_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.sphereSurfaceMeasure_isotropicSecondMoment
#print axioms TamesisNSCalderonZygmundKernelDefs.K_mean_zero_sphereSurfaceMeasure
#print axioms TamesisNSCalderonZygmundKernelDefs.czKernelClass_sphereSurfaceMeasure_K
