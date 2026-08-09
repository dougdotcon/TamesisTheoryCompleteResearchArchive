/-
LP-GAP-004 — the MATRIX Leray projector, lifted from `L²` to `H^s`.

Builds on two already-verified pieces: the matrix Fourier multiplier
`lerayOpL2` on `L²` vector fields (`TamesisLab.Foundations.LerayProjector`
/ `LerayOrthogonal`, closed and VERIFIED), and the isometric identification
`Hs E F s ≃ₗᵢ[ℂ] Lp F 2` via the Bessel potential
(`TamesisLab.Foundations.SobolevSpace`, closed and VERIFIED, blocked this
gap until FM-GAP-001 closed it). The construction is the exact conjugation
pattern already demonstrated in `SobolevSpace.lean` Step 6 for a SINGLE
scalar `L∞` multiplier (`fourierMultiplierSobolevCLM`), applied here to the
already-assembled MATRIX multiplier instead of a scalar one.

SCOPE, STATED EXPLICITLY: this file proves the operator is bounded,
idempotent, has norm exactly `1` (for `n ≥ 2`, nonzero) on `H^s`. It does
NOT prove self-adjointness or "orthogonal projection" on `H^s` — `Hs E F s`
in `SobolevSpace.lean` carries a `NormedSpace`/`CompleteSpace` structure,
not an inner product, so `ContinuousLinearMap.adjoint` is not even
statable on it yet. Transporting the inner product from `L²` through the
isometry `toL2ₗᵢ` would make that statable; that transport is NOT done
here and is registered as a new gap (`LP-GAP-005`), not claimed.
-/
import TamesisLab.Foundations.LerayOrthogonal
import TamesisLab.Foundations.SobolevSpace

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 1000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.LerayProjectorSobolev

open TamesisProbe
open TamesisLab.Foundations.SobolevSpace
open TamesisLab.Foundations.SobolevSpace.Hs

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable {n : ℕ}

/-! ## Step S1 : the operator, by conjugation through the `H^s ≃ₗᵢ L²` isometry. -/

/-- **THE MATRIX LERAY PROJECTOR ON `H^s`.** Defined by conjugating the already-verified
`L²` operator `lerayOpL2 b` through the isometric identification `Hs E F s ≃ₗᵢ[ℂ] Lp F 2`,
`F := EuclideanSpace ℂ (Fin n)` — the exact pattern already used for a scalar symbol in
`SobolevSpace.fourierMultiplierSobolevCLM`, here applied to the assembled matrix operator. -/
def lerayOpHs (b : OrthonormalBasis (Fin n) ℝ E) (s : ℝ) :
    Hs E (EuclideanSpace ℂ (Fin n)) s →L[ℂ] Hs E (EuclideanSpace ℂ (Fin n)) s :=
  (toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s).symm.toLinearIsometry.toContinuousLinearMap ∘L
    lerayOpL2 b ∘L (toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s).toLinearIsometry.toContinuousLinearMap

/-- The operator acts, on the `L²` representative, exactly by `lerayOpL2 b`. -/
@[simp] theorem toL2_lerayOpHs {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    toL2 (lerayOpHs b s f) = lerayOpL2 b (toL2 f) := by
  show toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s
      ((toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s).symm
        (lerayOpL2 b (toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s f))) = _
  rw [LinearIsometryEquiv.apply_symm_apply, toL2ₗᵢ_apply]

/-! ## Step S2 : idempotence transfers exactly. -/

/-- **THE `H^s` LERAY PROJECTOR IS IDEMPOTENT.** Transferred, not reproved: idempotence
is a statement purely about the operator's action, and `toL2` is injective. -/
theorem lerayOpHs_idem [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E) :
    (lerayOpHs b s) ∘L (lerayOpHs b s) = lerayOpHs b s := by
  refine ContinuousLinearMap.ext fun f => toL2_injective ?_
  show toL2 (lerayOpHs b s (lerayOpHs b s f)) = toL2 (lerayOpHs b s f)
  rw [toL2_lerayOpHs, toL2_lerayOpHs]
  simpa using DFunLike.congr_fun (lerayOpL2_idem b) (toL2 f)

/-! ## Step S3 : the operator norm transfers exactly, both directions, because `toL2` is a
surjective linear isometry (not merely a contraction). -/

theorem norm_lerayOpHs_apply {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    ‖lerayOpHs b s f‖ = ‖lerayOpL2 b (toL2 f)‖ := by
  rw [norm_def, toL2_lerayOpHs]

theorem norm_lerayOpHs_le [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖lerayOpHs b s‖ ≤ ‖lerayOpL2 b‖ := by
  refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun f => ?_
  rw [norm_lerayOpHs_apply, norm_def]
  exact (lerayOpL2 b).le_opNorm (toL2 f)

theorem norm_lerayOpL2_le_norm_lerayOpHs [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖lerayOpL2 b‖ ≤ ‖lerayOpHs b s‖ := by
  refine ContinuousLinearMap.opNorm_le_bound _ (norm_nonneg _) fun u => ?_
  set g : Hs E (EuclideanSpace ℂ (Fin n)) s :=
    (toL2ₗᵢ E (EuclideanSpace ℂ (Fin n)) s).symm u with hg
  have hu : toL2 g = u := by
    rw [hg, ← toL2ₗᵢ_apply, LinearIsometryEquiv.apply_symm_apply]
  calc ‖lerayOpL2 b u‖
      = ‖lerayOpL2 b (toL2 g)‖ := by rw [hu]
    _ = ‖toL2 (lerayOpHs b s g)‖ := by rw [toL2_lerayOpHs]
    _ = ‖lerayOpHs b s g‖ := (norm_def _).symm
    _ ≤ ‖lerayOpHs b s‖ * ‖g‖ := (lerayOpHs b s).le_opNorm _
    _ = ‖lerayOpHs b s‖ * ‖u‖ := by rw [norm_def, hu]

/-- **THE NORM TRANSFERS EXACTLY.** Not merely a bound: the `H^s` operator has exactly the
same operator norm as the already-verified `L²` operator, because conjugation by a surjective
linear isometry is norm-preserving in both directions. -/
theorem norm_lerayOpHs_eq [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E) :
    ‖lerayOpHs b s‖ = ‖lerayOpL2 b‖ :=
  le_antisymm (norm_lerayOpHs_le b) (norm_lerayOpL2_le_norm_lerayOpHs b)

/-- **THE `H^s` PROJECTOR IS A CONTRACTION OF NORM `≤ 1`**, transferred from the already-proved
optimal `L²` bound (`LerayOrthogonal.norm_lerayOpL2_le_one`, itself a correction of the earlier
`2n²` bound — see `LP-GAP-001`, closed). -/
theorem norm_lerayOpHs_le_one [Nontrivial E] {s : ℝ}
    (b : OrthonormalBasis (Fin n) ℝ E) : ‖lerayOpHs b s‖ ≤ 1 := by
  rw [norm_lerayOpHs_eq]
  exact TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_le_one b

/-! ## Step S4 : non-vacuity, transferred from the `L²` positive instance. -/

/-- `lerayOpHs` is nonzero exactly when `lerayOpL2` is nonzero — `toL2` is injective and
`toL2 (lerayOpHs b s f) = lerayOpL2 b (toL2 f)`, so a witness on one side transfers to the
other via `toL2_surjective`. -/
theorem lerayOpHs_ne_zero [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (hn : 2 ≤ n) : lerayOpHs b s ≠ 0 := by
  intro hzero
  obtain ⟨f, hf⟩ := ContinuousLinearMap.exists_ne_zero
    (TamesisLab.Foundations.LerayOrthogonal.lerayOpL2_ne_zero b hn)
  obtain ⟨g, hg⟩ := toL2_surjective f
  apply hf
  have : toL2 (lerayOpHs b s g) = lerayOpL2 b f := by rw [toL2_lerayOpHs, hg]
  rw [hzero, zero_apply, toL2_zero] at this
  exact this.symm

/-- **THE NORM ATTAINS EXACTLY `1` ON `H^s`, FOR `n ≥ 2`.** The `H^s` analogue of
`LerayOrthogonal.norm_lerayOpL2_eq_one_of_two_le`. -/
theorem norm_lerayOpHs_eq_one [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (hn : 2 ≤ n) : ‖lerayOpHs b s‖ = 1 := by
  rw [norm_lerayOpHs_eq]
  exact TamesisLab.Foundations.LerayOrthogonal.norm_lerayOpL2_eq_one b
    (TamesisLab.Foundations.LerayOrthogonal.lerayOpL2_ne_zero b hn)

/-! ## Step S5 : closed, hypothesis-light package, and the concrete anti-vacuity instance. -/

/-- **THE `H^s` MATRIX LERAY PROJECTOR PACKAGE.** Bounded, idempotent, norm exactly `1` for
`n ≥ 2`, nonzero. Self-adjointness / orthogonal-projection is explicitly NOT claimed — see the
file header and `LP-GAP-005`. -/
theorem lerayOpHs_package [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (hn : 2 ≤ n) :
    (lerayOpHs b s) ∘L (lerayOpHs b s) = lerayOpHs b s ∧
    ‖lerayOpHs b s‖ = 1 ∧
    lerayOpHs b s ≠ 0 :=
  ⟨lerayOpHs_idem b, norm_lerayOpHs_eq_one b hn, lerayOpHs_ne_zero b hn⟩

/-- Concrete, hypothesis-free instance on `ℝ³` at `s = 5/2`: no free variables beyond the
orthonormal basis, cannot be vacuous. Mirrors `SobolevSpace.concrete_leray_operator` and
`LerayOrthogonal.leray_R3_orthogonal_projector`. -/
theorem concrete_lerayOpHs_R3 (b3 : OrthonormalBasis (Fin 3) ℝ (EuclideanSpace ℝ (Fin 3))) :
    (lerayOpHs b3 (5 / 2 : ℝ)) ∘L (lerayOpHs b3 (5 / 2 : ℝ)) = lerayOpHs b3 (5 / 2 : ℝ) ∧
    ‖lerayOpHs b3 (5 / 2 : ℝ)‖ = 1 ∧
    lerayOpHs b3 (5 / 2 : ℝ) ≠ 0 :=
  lerayOpHs_package b3 (by norm_num)

end TamesisLab.Foundations.LerayProjectorSobolev

open TamesisLab.Foundations.LerayProjectorSobolev

#print axioms TamesisLab.Foundations.LerayProjectorSobolev.lerayOpHs
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.toL2_lerayOpHs
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.lerayOpHs_idem
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.norm_lerayOpHs_eq
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.norm_lerayOpHs_le_one
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.lerayOpHs_ne_zero
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.norm_lerayOpHs_eq_one
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.lerayOpHs_package
#print axioms TamesisLab.Foundations.LerayProjectorSobolev.concrete_lerayOpHs_R3
