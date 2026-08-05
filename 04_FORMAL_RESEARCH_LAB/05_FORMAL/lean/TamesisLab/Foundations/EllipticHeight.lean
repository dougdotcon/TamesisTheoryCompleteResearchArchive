import Mathlib.AlgebraicGeometry.EllipticCurve.Affine.AddSubMap
import Mathlib.NumberTheory.Height.EllipticCurve
import Mathlib.NumberTheory.Height.NumberField
import Mathlib.GroupTheory.Descent

/-!
# Obrigação D da Peça C, mecânica, sem prova incompleta

`D : ∀ P Q, ∃ c ≠ 0, (fun i ↦ (addSubMap W i).eval (sym2x P Q)) = c • sym2x (P+Q) (P-Q)`

Fecha o TODO de `Mathlib/AlgebraicGeometry/EllipticCurve/Affine/AddSubMap.lean`
("Show that the map really does what it is claimed to do") no nível de x-coordenadas.
-/

open MvPolynomial WeierstrassCurve WeierstrassCurve.Affine WeierstrassCurve.Affine.Point

set_option linter.unusedSectionVars false
set_option maxHeartbeats 2000000

namespace TamesisLab.Foundations.EllipticHeight

variable {F : Type*} [Field F] [DecidableEq F] {W : Affine F}

/-! ### plumbing -/

lemma smul_vec3 (c b₀ b₁ b₂ : F) : c • (![b₀, b₁, b₂] : Fin 3 → F) = ![c * b₀, c * b₁, c * b₂] := by
  funext i; fin_cases i <;> simp

lemma vec3_eq {a₀ a₁ a₂ b₀ b₁ b₂ : F} (h₀ : a₀ = b₀) (h₁ : a₁ = b₁) (h₂ : a₂ = b₂) :
    (![a₀, a₁, a₂] : Fin 3 → F) = ![b₀, b₁, b₂] := by rw [h₀, h₁, h₂]

lemma eval0 (a b c : F) :
    (addSubMap W 0).eval ![a, b, c] = a ^ 2 - W.b₄ * a * c - W.b₆ * b * c - W.b₈ * c ^ 2 := by
  simp [addSubMap]

lemma eval1 (a b c : F) :
    (addSubMap W 1).eval ![a, b, c] = 2 * b * a + W.b₂ * a * c + W.b₄ * b * c + W.b₆ * c ^ 2 := by
  simp [addSubMap]

lemma eval2 (a b c : F) : (addSubMap W 2).eval ![a, b, c] = b ^ 2 - 4 * a * c := by
  simp [addSubMap]

lemma evalAt (a b c : F) :
    (fun i ↦ (addSubMap W i).eval ![a, b, c]) =
      ![a ^ 2 - W.b₄ * a * c - W.b₆ * b * c - W.b₈ * c ^ 2,
        2 * b * a + W.b₂ * a * c + W.b₄ * b * c + W.b₆ * c ^ 2,
        b ^ 2 - 4 * a * c] := by
  funext i
  fin_cases i <;> simp [addSubMap]

/-! ### the duplication input `![x*x, x+x, 1]` -/

variable [W.IsElliptic]

lemma dupMain (x y : F) (h : W.Nonsingular x y) :
    ∃ c : F, c ≠ 0 ∧
      (fun i ↦ (addSubMap W i).eval ![x * x, x + x, 1]) =
        c • ((0 : W.Point).sym2x (some x y h + some x y h)) := by
  have heq : y ^ 2 + W.a₁ * x * y + W.a₃ * y = x ^ 3 + W.a₂ * x ^ 2 + W.a₄ * x + W.a₆ :=
    (W.equation_iff x y).mp h.1
  have hA2 : (x + x) ^ 2 - 4 * (x * x) * (1 : F) = 0 := by ring
  by_cases hψ : y = W.negY x y
  · -- `2 • P = 0`
    have hψ' : 2 * y + W.a₁ * x + W.a₃ = 0 := by
      simp only [WeierstrassCurve.Affine.negY] at hψ; linear_combination hψ
    have hA1 : 2 * (x + x) * (x * x) + W.b₂ * (x * x) * 1 + W.b₄ * (x + x) * 1
        + W.b₆ * (1 : F) ^ 2 = 0 := by
      simp only [WeierstrassCurve.b₂, WeierstrassCurve.b₄, WeierstrassCurve.b₆]
      linear_combination (2 * y + W.a₁ * x + W.a₃) * hψ' - 4 * heq
    have hf1 : (addSubMap W 1).eval ![x * x, x + x, (1 : F)] = 0 := by rw [eval1]; exact hA1
    have hf2 : (addSubMap W 2).eval ![x * x, x + x, (1 : F)] = 0 := by rw [eval2]; exact hA2
    have hf0 : (addSubMap W 0).eval ![x * x, x + x, (1 : F)] ≠ 0 := by
      intro h0
      have hc := addSubMapCoeff_condition W ![x * x, x + x, (1 : F)] 2
      rw [Fin.sum_univ_three, h0, hf1, hf2] at hc
      simp at hc
    refine ⟨_, hf0, ?_⟩
    rw [add_self_of_Y_eq hψ, sym2x_zero_zero, evalAt, eval0, smul_vec3]
    exact vec3_eq (by ring) (by rw [hA1]; ring) (by rw [hA2]; ring)
  · -- `2 • P ≠ 0`
    have hd : y - W.negY x y ≠ 0 := sub_ne_zero.mpr hψ
    have hψ' : 2 * y + W.a₁ * x + W.a₃ ≠ 0 := by
      simp only [WeierstrassCurve.Affine.negY] at hd
      intro hc; exact hd (by linear_combination hc)
    have hA1 : 2 * (x + x) * (x * x) + W.b₂ * (x * x) * 1 + W.b₄ * (x + x) * 1
        + W.b₆ * (1 : F) ^ 2 = (2 * y + W.a₁ * x + W.a₃) ^ 2 := by
      simp only [WeierstrassCurve.b₂, WeierstrassCurve.b₄, WeierstrassCurve.b₆]
      linear_combination (-4 : F) * heq
    have hx₃ : (2 * y + W.a₁ * x + W.a₃) ^ 2 * W.addX x x (W.slope x x y y) =
        (3 * x ^ 2 + 2 * W.a₂ * x + W.a₄ - W.a₁ * y) ^ 2
          + W.a₁ * (3 * x ^ 2 + 2 * W.a₂ * x + W.a₄ - W.a₁ * y) * (2 * y + W.a₁ * x + W.a₃)
          - (W.a₂ + 2 * x) * (2 * y + W.a₁ * x + W.a₃) ^ 2 := by
      have hden : y - W.negY x y = 2 * y + W.a₁ * x + W.a₃ := by
        simp only [WeierstrassCurve.Affine.negY]; ring
      rw [slope_of_Y_ne rfl hψ, hden]
      simp only [WeierstrassCurve.Affine.addX]
      field_simp
      ring
    refine ⟨2 * (x + x) * (x * x) + W.b₂ * (x * x) * 1 + W.b₄ * (x + x) * 1 + W.b₆ * (1 : F) ^ 2,
      by rw [hA1]; exact pow_ne_zero 2 hψ', ?_⟩
    rw [add_self_of_Y_ne hψ, sym2x_zero_some, evalAt, smul_vec3]
    refine vec3_eq ?_ (by ring) (by rw [hA2]; ring)
    rw [hA1]
    simp only [WeierstrassCurve.b₄, WeierstrassCurve.b₆, WeierstrassCurve.b₈]
    linear_combination (-1 : F) * hx₃ + (4 * W.a₂ + W.a₁ ^ 2 + 8 * x) * heq

/-! ### obligation D -/

theorem addSubMap_eval_sym2x (P Q : W.Point) :
    ∃ c : F, c ≠ 0 ∧
      (fun i ↦ (addSubMap W i).eval (P.sym2x Q)) = c • ((P + Q).sym2x (P - Q)) := by
  rcases P with _ | ⟨x₁, y₁, h₁⟩ <;> rcases Q with _ | ⟨x₂, y₂, h₂⟩
  · -- (0, 0)
    refine ⟨1, one_ne_zero, ?_⟩
    simp only [← zero_def, add_zero, sub_zero, sym2x_zero_zero, evalAt, smul_vec3]
    exact vec3_eq (by ring) (by ring) (by ring)
  · -- (0, some)
    refine ⟨1, one_ne_zero, ?_⟩
    rw [← zero_def, sym2x_zero_some, zero_add, zero_sub, neg_some, sym2x_some_some, evalAt,
      smul_vec3]
    exact vec3_eq (by ring) (by ring) (by ring)
  · -- (some, 0)
    refine ⟨1, one_ne_zero, ?_⟩
    rw [← zero_def, sym2x_some_zero, add_zero, sub_zero, sym2x_some_some, evalAt, smul_vec3]
    exact vec3_eq (by ring) (by ring) (by ring)
  · -- (some, some)
    by_cases hx : x₁ = x₂
    · subst hx
      rcases Y_eq_of_X_eq h₁.1 h₂.1 rfl with rfl | hy
      · rw [show (some x₁ y₁ h₂ : W.Point) = some x₁ y₁ h₁ from rfl, sym2x_some_some, sub_self,
          sym2x_comm]
        exact dupMain x₁ y₁ h₁
      · subst hy
        rw [show (some x₁ (W.negY x₁ y₂) h₁ : W.Point) = -(some x₁ y₂ h₂) from rfl,
          sym2x_neg_left, sym2x_some_some, neg_add_cancel, sub_eq_add_neg, ← neg_add,
          sym2x_neg_right]
        exact dupMain x₁ y₂ h₂
    · -- generic branch
      have hd : x₁ - x₂ ≠ 0 := sub_ne_zero.mpr hx
      have hne : ¬(x₁ = x₂ ∧ y₁ = W.negY x₂ y₂) := fun h => hx h.1
      have hne' : ¬(x₁ = x₂ ∧ y₁ = W.negY x₂ (W.negY x₂ y₂)) := fun h => hx h.1
      have e₁ : y₁ ^ 2 + W.a₁ * x₁ * y₁ + W.a₃ * y₁
          = x₁ ^ 3 + W.a₂ * x₁ ^ 2 + W.a₄ * x₁ + W.a₆ := (W.equation_iff x₁ y₁).mp h₁.1
      have e₂ : y₂ ^ 2 + W.a₁ * x₂ * y₂ + W.a₃ * y₂
          = x₂ ^ 3 + W.a₂ * x₂ ^ 2 + W.a₄ * x₂ + W.a₆ := (W.equation_iff x₂ y₂).mp h₂.1
      have hx₃ : (x₁ - x₂) ^ 2 * W.addX x₁ x₂ (W.slope x₁ x₂ y₁ y₂)
          = (y₁ - y₂) ^ 2 + W.a₁ * (y₁ - y₂) * (x₁ - x₂)
            - (W.a₂ + x₁ + x₂) * (x₁ - x₂) ^ 2 := by
        rw [slope_of_X_ne hx]
        simp only [WeierstrassCurve.Affine.addX]
        field_simp
        ring
      have hx₄ : (x₁ - x₂) ^ 2 * W.addX x₁ x₂ (W.slope x₁ x₂ y₁ (W.negY x₂ y₂))
          = (y₁ + y₂ + W.a₁ * x₂ + W.a₃) ^ 2
            + W.a₁ * (y₁ + y₂ + W.a₁ * x₂ + W.a₃) * (x₁ - x₂)
            - (W.a₂ + x₁ + x₂) * (x₁ - x₂) ^ 2 := by
        rw [slope_of_X_ne hx]
        simp only [WeierstrassCurve.Affine.addX, WeierstrassCurve.Affine.negY]
        field_simp
        ring
      rw [sym2x_some_some, sub_eq_add_neg, neg_some, add_some hne, add_some hne',
        sym2x_some_some, evalAt]
      refine ⟨(x₁ - x₂) ^ 2, pow_ne_zero 2 hd, ?_⟩
      rw [smul_vec3]
      refine vec3_eq ?_ ?_ (by ring)
      · -- product
        simp only [WeierstrassCurve.b₄, WeierstrassCurve.b₆, WeierstrassCurve.b₈]
        refine mul_left_cancel₀ (pow_ne_zero 2 hd) ?_
        linear_combination
          (-((x₁ - x₂) ^ 2 * W.addX x₁ x₂ (W.slope x₁ x₂ y₁ (W.negY x₂ y₂)))) * hx₃
          + (-((y₁ - y₂) ^ 2 + W.a₁ * (y₁ - y₂) * (x₁ - x₂)
              - (W.a₂ + x₁ + x₂) * (x₁ - x₂) ^ 2)) * hx₄
          + (-(W.a₆ - 2 * y₂ * W.a₃ - 2 * y₂ ^ 2 + y₁ * W.a₃ + y₁ ^ 2 - x₂ * W.a₁ * W.a₃
              - 2 * x₂ * y₂ * W.a₁ - 2 * x₂ ^ 2 * W.a₂ - x₂ ^ 2 * W.a₁ ^ 2 - 2 * x₂ ^ 3
              + x₁ * W.a₄ + x₁ * W.a₁ * W.a₃ + x₁ * y₁ * W.a₁ + 4 * x₁ * x₂ * W.a₂
              + x₁ * x₂ * W.a₁ ^ 2 + 2 * x₁ * x₂ ^ 2 - x₁ ^ 2 * W.a₂ + 2 * x₁ ^ 2 * x₂
              - x₁ ^ 3)) * e₁
          + (-(-W.a₆ + y₂ * W.a₃ + y₂ ^ 2 + x₂ * W.a₄ + x₂ * W.a₁ * W.a₃ + x₂ * y₂ * W.a₁
              - x₂ ^ 2 * W.a₂ - x₂ ^ 3 - 2 * x₁ * W.a₄ - x₁ * W.a₁ * W.a₃ + 4 * x₁ * x₂ * W.a₂
              + x₁ * x₂ * W.a₁ ^ 2 + 2 * x₁ * x₂ ^ 2 - 4 * x₁ ^ 2 * W.a₂ - x₁ ^ 2 * W.a₁ ^ 2
              + 2 * x₁ ^ 2 * x₂ - 4 * x₁ ^ 3)) * e₂
      · -- sum
        simp only [WeierstrassCurve.b₂, WeierstrassCurve.b₄, WeierstrassCurve.b₆]
        linear_combination (-1 : F) * hx₃ + (-1 : F) * hx₄ + (-2 : F) * e₁ + (-2 : F) * e₂

end TamesisLab.Foundations.EllipticHeight

/-! ## Corolários: lei do paralelogramo e finitude da torção (agora INCONDICIONAIS) -/

namespace TamesisLab.Foundations.EllipticHeight.Descent

open Height

variable {K : Type*} [Field K] [DecidableEq K] [Height.AdmissibleAbsValues K]

/-- Altura logarítmica ingênua de um ponto afim: `h(P) = h(x(P))`. -/
noncomputable def naiveH {W : WeierstrassCurve K} (P : W.toAffine.Point) : ℝ :=
  Height.logHeight P.xRep

theorem naiveH_nonneg {W : WeierstrassCurve K} (P : W.toAffine.Point) : 0 ≤ naiveH P :=
  Height.logHeight_nonneg _

private lemma xRep_eta {W : WeierstrassCurve K} (P : W.toAffine.Point) :
    ![P.xRep 0, P.xRep 1] = P.xRep := by
  ext i; fin_cases i <;> rfl

theorem abs_logHeight_sym2x_sub_le (W : WeierstrassCurve K) :
    ∃ C, ∀ P Q : W.toAffine.Point,
      |Height.logHeight (P.sym2x Q) - (naiveH P + naiveH Q)| ≤ C := by
  obtain ⟨C, hC⟩ := Height.abs_logHeight_sym2_sub_le K
  refine ⟨C, fun P Q ↦ ?_⟩
  have hP : ![P.xRep 0, P.xRep 1] ≠ 0 := by rw [xRep_eta]; exact P.xRep_ne_zero
  have hQ : ![Q.xRep 0, Q.xRep 1] ≠ 0 := by rw [xRep_eta]; exact Q.xRep_ne_zero
  have h := hC hP hQ
  rw [xRep_eta, xRep_eta] at h
  exact h

/-- **Lei do paralelogramo aproximada** — incondicional, via a obrigação D provada acima. -/
theorem parallelogram (W : WeierstrassCurve K) [W.IsElliptic] :
    ∃ C, ∀ P Q : W.toAffine.Point,
      |naiveH (P + Q) + naiveH (P - Q) - 2 * (naiveH P + naiveH Q)| ≤ C := by
  obtain ⟨C₁, hC₁⟩ := W.abs_logHeight_addSubMap_sub_two_mul_logHeight_le
  obtain ⟨C₂, hC₂⟩ := abs_logHeight_sym2x_sub_le W
  refine ⟨C₁ + C₂ + 2 * C₂, fun P Q ↦ ?_⟩
  obtain ⟨c, hc, hcE⟩ := TamesisLab.Foundations.EllipticHeight.addSubMap_eval_sym2x P Q
  have hscal : Height.logHeight (fun i ↦ (MvPolynomial.eval (P.sym2x Q)) (W.addSubMap i))
      = Height.logHeight ((P + Q).sym2x (P - Q)) := by
    rw [hcE, Height.logHeight_smul_eq_logHeight _ hc]
  have h1 := hC₁ (P.sym2x Q)
  have h2 := hC₂ P Q
  have h3 := hC₂ (P + Q) (P - Q)
  rw [hscal] at h1
  rw [abs_le] at h1 h2 h3 ⊢
  constructor <;> linarith [h1.1, h1.2, h2.1, h2.2, h3.1, h3.2]

/-- Coordenada x afim do ponto (0 no ponto no infinito). -/
noncomputable def xC {W : WeierstrassCurve K} (P : W.toAffine.Point) : K :=
  P.xRep 0 / P.xRep 1

theorem naiveH_eq_logHeight₁_xC {W : WeierstrassCurve K} (P : W.toAffine.Point) :
    naiveH P = Height.logHeight₁ (xC P) := by
  cases P with
  | zero => simp [naiveH, xC, WeierstrassCurve.Affine.Point.xRep]
  | some x y h =>
      simp [naiveH, xC, WeierstrassCurve.Affine.Point.xRep, Height.logHeight₁_eq_logHeight]

private lemma xC_some {W : WeierstrassCurve K} {x y : K} (h : W.toAffine.Nonsingular x y) :
    xC (WeierstrassCurve.Affine.Point.some x y h) = x := by
  simp [xC, WeierstrassCurve.Affine.Point.xRep]

/-- As fibras do mapa x são finitas (≤ 3 pontos). -/
instance tendstoCofinite_xC {W : WeierstrassCurve K} :
    Filter.TendstoCofinite (xC (W := W)) := by
  classical
  rw [Filter.tendstoCofinite_iff_finite_preimage_singleton]
  intro t
  rcases Set.eq_empty_or_nonempty {P : W.toAffine.Point | xC P = t ∧ P ≠ 0} with
    hE | ⟨P₀, hP₀t, hP₀0⟩
  · refine (Set.finite_singleton (0 : W.toAffine.Point)).subset fun P hP ↦ ?_
    simp only [Set.mem_preimage, Set.mem_singleton_iff] at hP ⊢
    by_contra hne
    have hmem : P ∈ {P : W.toAffine.Point | xC P = t ∧ P ≠ 0} := ⟨hP, hne⟩
    rw [hE] at hmem
    exact hmem
  · refine (((Set.finite_singleton P₀).insert (-P₀)).insert 0).subset fun P hP ↦ ?_
    simp only [Set.mem_preimage, Set.mem_singleton_iff] at hP
    rcases P with _ | ⟨x, y, hxy⟩
    · exact Or.inl rfl
    rcases P₀ with _ | ⟨x₀, y₀, hxy₀⟩
    · exact absurd rfl hP₀0
    rw [xC_some] at hP
    rw [xC_some] at hP₀t
    have hx : x = x₀ := hP.trans hP₀t.symm
    rcases (WeierstrassCurve.Affine.Point.X_eq_iff (h₁ := hxy) (h₂ := hxy₀)).mp hx with h | h
    · exact Or.inr (Or.inr h)
    · exact Or.inr (Or.inl h)

instance northcott_naiveH {W : WeierstrassCurve K}
    [Northcott (Height.logHeight₁ (K := K))] [Filter.TendstoCofinite (xC (W := W))] :
    Northcott (naiveH (W := W)) := by
  have h : (naiveH (W := W)) = Height.logHeight₁ ∘ xC := funext naiveH_eq_logHeight₁_xC
  rw [h]
  exact Northcott.comp_of_finite_fibers _ _

/-- **Finitude da torção de `E(K)`** — incondicional para `K` com Northcott
(em particular `K = ℚ`), sem qualquer forma de Mordell-Weil fraco. -/
theorem torsion_finite (W : WeierstrassCurve K) [W.IsElliptic]
    [Northcott (Height.logHeight₁ (K := K))] :
    Finite (AddCommGroup.torsion W.toAffine.Point) := by
  obtain ⟨C, hC⟩ := parallelogram W
  exact AddCommGroup.finite_torsion_of_descent' hC

/-- Peça C ainda condicional a **F** (Mordell-Weil fraco), agora com D descarregada. -/
theorem pecaC_conditional_on_F (W : WeierstrassCurve K) [W.IsElliptic]
    [Northcott (Height.logHeight₁ (K := K))]
    (hWMW : (nsmulAddMonoidHom (α := W.toAffine.Point) 2).range.FiniteIndex) :
    AddGroup.FG W.toAffine.Point := by
  obtain ⟨C, hC⟩ := parallelogram W
  exact AddCommGroup.fg_of_descent' (C := C) hWMW (fun P ↦ naiveH_nonneg P) hC

end TamesisLab.Foundations.EllipticHeight.Descent

/-! ## Instância positiva: `y² = x³ + 1` sobre ℚ (a hipótese NÃO é vácua) -/

noncomputable def Wq : WeierstrassCurve ℚ := ⟨0, 0, 0, 0, 1⟩

instance : Wq.IsElliptic := by
  constructor
  rw [isUnit_iff_ne_zero]
  simp [Wq, WeierstrassCurve.Δ, WeierstrassCurve.b₂, WeierstrassCurve.b₄,
    WeierstrassCurve.b₆, WeierstrassCurve.b₈]

theorem Wq_ns_2_3 : Wq.toAffine.Nonsingular 2 3 :=
  (WeierstrassCurve.Affine.equation_iff_nonsingular).mp
    (by rw [WeierstrassCurve.Affine.equation_iff]; norm_num [Wq])

theorem Wq_ns_0_1 : Wq.toAffine.Nonsingular 0 1 :=
  (WeierstrassCurve.Affine.equation_iff_nonsingular).mp
    (by rw [WeierstrassCurve.Affine.equation_iff]; norm_num [Wq])

noncomputable def Pa : Wq.toAffine.Point := .some 2 3 Wq_ns_2_3
noncomputable def Pb : Wq.toAffine.Point := .some 0 1 Wq_ns_0_1

/-- Testemunhas: o grupo NÃO é trivial, logo D e os corolários não são vácuos. -/
theorem Pa_ne_zero : Pa ≠ 0 := WeierstrassCurve.Affine.Point.some_ne_zero _
theorem Pb_ne_zero : Pb ≠ 0 := WeierstrassCurve.Affine.Point.some_ne_zero _
theorem Pa_ne_Pb : Pa ≠ Pb := by simp [Pa, Pb]

/-- D instanciada num par concreto de pontos distintos e não nulos. -/
theorem D_at_Pa_Pb : ∃ c : ℚ, c ≠ 0 ∧
    (fun i ↦ (MvPolynomial.eval (Pa.sym2x Pb)) (Wq.addSubMap i)) = c • ((Pa + Pb).sym2x (Pa - Pb)) :=
  TamesisLab.Foundations.EllipticHeight.addSubMap_eval_sym2x Pa Pb

/-- O lado esquerdo de D nesse par é `![-8, 4, 4] ≠ 0`; logo `sym2x (Pa+Pb) (Pa-Pb) ≠ 0`
e a igualdade de D não é degenerada. -/
theorem D_lhs_at_Pa_Pb :
    (fun i ↦ (MvPolynomial.eval (Pa.sym2x Pb)) (Wq.addSubMap i)) = ![-8, 4, 4] := by
  funext i
  fin_cases i <;>
    simp [WeierstrassCurve.addSubMap, Pa, Pb, WeierstrassCurve.Affine.Point.sym2x,
      WeierstrassCurve.Affine.Point.xRep, Wq, WeierstrassCurve.b₂, WeierstrassCurve.b₄,
      WeierstrassCurve.b₆, WeierstrassCurve.b₈] <;>
    norm_num

theorem Wq_torsion_finite : Finite (AddCommGroup.torsion Wq.toAffine.Point) :=
  TamesisLab.Foundations.EllipticHeight.Descent.torsion_finite Wq

theorem Wq_parallelogram : ∃ C, ∀ P Q : Wq.toAffine.Point,
    |TamesisLab.Foundations.EllipticHeight.Descent.naiveH (P + Q) + TamesisLab.Foundations.EllipticHeight.Descent.naiveH (P - Q)
      - 2 * (TamesisLab.Foundations.EllipticHeight.Descent.naiveH P + TamesisLab.Foundations.EllipticHeight.Descent.naiveH Q)| ≤ C :=
  TamesisLab.Foundations.EllipticHeight.Descent.parallelogram Wq

#print axioms TamesisLab.Foundations.EllipticHeight.addSubMap_eval_sym2x
#print axioms TamesisLab.Foundations.EllipticHeight.dupMain
#print axioms TamesisLab.Foundations.EllipticHeight.Descent.parallelogram
#print axioms TamesisLab.Foundations.EllipticHeight.Descent.torsion_finite
#print axioms TamesisLab.Foundations.EllipticHeight.Descent.pecaC_conditional_on_F
#print axioms D_at_Pa_Pb
#print axioms D_lhs_at_Pa_Pb
#print axioms Wq_torsion_finite
#print axioms Wq_parallelogram
