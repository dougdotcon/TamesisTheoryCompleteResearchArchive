/-
LP-GAP-005 — self-adjointness / orthogonal projection of the Leray operator on `H^s`.

`Hs E F s` (`SobolevSpace.lean`) carries `NormedSpace`/`CompleteSpace`, not an
`InnerProductSpace` instance — so `ContinuousLinearMap.adjoint` / `IsSelfAdjoint`
are not directly statable on it. Mathlib does have a generic transport tool,
`InnerProductSpace.induced`, but it requires the ALREADY-installed norm on the
domain to be definitionally the specific `SeminormedAddCommGroup.induced` instance
built from the SAME map used to induce the inner product. `Hs`'s norm was installed
in `SobolevSpace.lean` via `NormedAddCommGroup.induced (Hs E F s) (Lp F 2 ...)
(toL2AddHom E F s) toL2_injective`, using an `AddMonoidHom`, not a `LinearMap`, and
matching that instance up with `InnerProductSpace.induced`'s expectations risks a
silent instance diamond — two definitionally-but-not-syntactically-equal
`SeminormedAddCommGroup (Hs E F s)` instances, which can make later lemmas fail to
apply or, worse, apply to the wrong instance without any error.

SCOPE, STATED EXPLICITLY: rather than risk that diamond, this file proves the
mathematical content of "self-adjoint orthogonal projection" directly, via the
explicit PULLBACK PAIRING `hsInner f g := inner ℂ (toL2 f) (toL2 g)` — a plain
`ℂ`-valued function, not a competing type class instance. This is a faithful,
rigorous statement of self-adjointness (`⟪Tf,g⟫ = ⟪f,Tg⟫` for all `f g`) and of
orthogonal projection (range of `P` orthogonal to range of `1 - P`, Pythagoras),
just not phrased through Mathlib's `IsSelfAdjoint`/`ContinuousLinearMap.adjoint`
API, which would require installing that instance. Registering `Hs E F s` as a
global `InnerProductSpace` is NOT done here and remains open work if ever wanted.
-/
import TamesisLab.Foundations.LerayProjectorSobolev

open MeasureTheory FourierTransform ENNReal TemperedDistribution Filter
open scoped SchwartzMap Topology

set_option maxHeartbeats 1000000
set_option linter.unusedSectionVars false

noncomputable section

namespace TamesisLab.Foundations.LerayOrthogonalSobolev

open TamesisProbe
open TamesisLab.Foundations.SobolevSpace
open TamesisLab.Foundations.SobolevSpace.Hs
open TamesisLab.Foundations.LerayProjectorSobolev

variable {E : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [MeasurableSpace E] [BorelSpace E]

variable {n : ℕ}

/-- `toL2` respects subtraction — not among `SobolevSpace.lean`'s bundled lemmas
(only `toL2_add`/`toL2_zero`/`toL2_smul` are given there), derived here from the
bundled linear map `toL2ₗ`, for which `map_sub` is a generic fact. -/
theorem toL2_sub {s : ℝ} (f g : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    toL2 (f - g) = toL2 f - toL2 g :=
  map_sub (toL2ₗ E (EuclideanSpace ℂ (Fin n)) s) f g

/-! ## Step O1 : the pullback pairing. -/

/-- **THE PULLBACK INNER PRODUCT ON `H^s`**, as a plain function (not a competing
`InnerProductSpace` instance — see the file header for why). Defined by pulling
the `L²` inner product back along `toL2`. -/
def hsInner {s : ℝ} (f g : Hs E (EuclideanSpace ℂ (Fin n)) s) : ℂ :=
  inner ℂ (toL2 f) (toL2 g)

/-- The pairing genuinely represents the `H^s` norm: `hsInner f f = ‖f‖²` (as a
complex number with zero imaginary part, matching the standard `L²` identity). -/
theorem hsInner_self_eq_normSq {s : ℝ} (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    hsInner f f = (‖f‖ ^ 2 : ℝ) := by
  rw [hsInner, norm_def, inner_self_eq_norm_sq_to_K]
  simp

/-! ## Step O2 : self-adjointness, transferred via `toL2_lerayOpHs`. -/

/-- **THE `H^s` LERAY PROJECTOR IS SELF-ADJOINT** with respect to the pullback
pairing `hsInner` — the `H^s` analogue of `LerayOrthogonal.inner_lerayOpL2_symm`,
obtained by transfer, not reproved from scratch. -/
theorem hsInner_lerayOpHs_symm [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f g : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    hsInner (lerayOpHs b s f) g = hsInner f (lerayOpHs b s g) := by
  rw [hsInner, hsInner, toL2_lerayOpHs, toL2_lerayOpHs]
  exact TamesisLab.Foundations.LerayOrthogonal.inner_lerayOpL2_symm b (toL2 f) (toL2 g)

/-- `hsInner (P f) (P f) = hsInner f (P f)` — the `H^s` analogue of
`LerayOrthogonal.inner_self_lerayOpL2`, from idempotence and self-adjointness. -/
theorem hsInner_self_lerayOpHs [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    hsInner (lerayOpHs b s f) (lerayOpHs b s f) = hsInner f (lerayOpHs b s f) := by
  conv_lhs => rw [hsInner_lerayOpHs_symm b f (lerayOpHs b s f)]
  have h := DFunLike.congr_fun (lerayOpHs_idem b (s := s)) f
  simpa using congrArg (hsInner f) h

/-! ## Step O3 : `P` is an orthogonal projection on `H^s`; Pythagoras. -/

/-- The range of `P` is orthogonal to the range of `1 - P`, with respect to
`hsInner` — the `H^s` analogue of `LerayOrthogonal.inner_lerayOpL2_sub`. -/
theorem hsInner_lerayOpHs_sub [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    hsInner (lerayOpHs b s f) (f - lerayOpHs b s f) = 0 := by
  rw [hsInner, toL2_lerayOpHs, toL2_sub, toL2_lerayOpHs]
  exact TamesisLab.Foundations.LerayOrthogonal.inner_lerayOpL2_sub b (toL2 f)

/-- **PYTHAGORAS ON `H^s`.** `‖f‖² = ‖P f‖² + ‖f − P f‖²` — proved directly by
transferring the norm through `toL2`, which is linear and isometric, reducing to
the already-verified `L²` Pythagoras identity. -/
theorem norm_sq_lerayOpHs_pythagoras [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (f : Hs E (EuclideanSpace ℂ (Fin n)) s) :
    ‖f‖ ^ 2 = ‖lerayOpHs b s f‖ ^ 2 + ‖f - lerayOpHs b s f‖ ^ 2 := by
  have hsub : toL2 (f - lerayOpHs b s f) = toL2 f - lerayOpL2 b (toL2 f) := by
    rw [toL2_sub, toL2_lerayOpHs]
  rw [norm_def, norm_lerayOpHs_apply, norm_def, hsub]
  exact TamesisLab.Foundations.LerayOrthogonal.norm_sq_lerayOpL2_pythagoras b (toL2 f)

/-! ## Step O4 : closed package and the concrete anti-vacuity instance. -/

/-- **THE `H^s` LERAY PROJECTOR IS A SELF-ADJOINT ORTHOGONAL PROJECTION**, with
respect to the pullback pairing `hsInner` (see file header for why this is not
phrased through Mathlib's `IsSelfAdjoint` type class). Combines
`lerayOpHs_package` (bounded, idempotent, norm 1, nonzero) with self-adjointness
and Pythagoras proved in this file. -/
theorem lerayOpHs_orthogonal_package [Nontrivial E] {s : ℝ} (b : OrthonormalBasis (Fin n) ℝ E)
    (hn : 2 ≤ n) :
    (lerayOpHs b s) ∘L (lerayOpHs b s) = lerayOpHs b s ∧
    ‖lerayOpHs b s‖ = 1 ∧
    lerayOpHs b s ≠ 0 ∧
    (∀ f g, hsInner (lerayOpHs b s f) g = hsInner f (lerayOpHs b s g)) ∧
    (∀ f, hsInner (lerayOpHs b s f) (f - lerayOpHs b s f) = 0) ∧
    (∀ f, ‖f‖ ^ 2 = ‖lerayOpHs b s f‖ ^ 2 + ‖f - lerayOpHs b s f‖ ^ 2) :=
  ⟨lerayOpHs_idem b, norm_lerayOpHs_eq_one b hn, lerayOpHs_ne_zero b hn,
   fun f g => hsInner_lerayOpHs_symm b f g,
   fun f => hsInner_lerayOpHs_sub b f,
   fun f => norm_sq_lerayOpHs_pythagoras b f⟩

/-- Concrete, hypothesis-free instance on `ℝ³` at `s = 5/2`. -/
theorem concrete_lerayOpHs_orthogonal_R3
    (b3 : OrthonormalBasis (Fin 3) ℝ (EuclideanSpace ℝ (Fin 3))) :
    (lerayOpHs b3 (5 / 2 : ℝ)) ∘L (lerayOpHs b3 (5 / 2 : ℝ)) = lerayOpHs b3 (5 / 2 : ℝ) ∧
    ‖lerayOpHs b3 (5 / 2 : ℝ)‖ = 1 ∧
    lerayOpHs b3 (5 / 2 : ℝ) ≠ 0 ∧
    (∀ f g, hsInner (lerayOpHs b3 (5 / 2 : ℝ) f) g
      = hsInner f (lerayOpHs b3 (5 / 2 : ℝ) g)) ∧
    (∀ f, hsInner (lerayOpHs b3 (5 / 2 : ℝ) f) (f - lerayOpHs b3 (5 / 2 : ℝ) f) = 0) ∧
    (∀ f, ‖f‖ ^ 2 = ‖lerayOpHs b3 (5 / 2 : ℝ) f‖ ^ 2
      + ‖f - lerayOpHs b3 (5 / 2 : ℝ) f‖ ^ 2) :=
  lerayOpHs_orthogonal_package b3 (by norm_num)

end TamesisLab.Foundations.LerayOrthogonalSobolev

open TamesisLab.Foundations.LerayOrthogonalSobolev

#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.hsInner
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.hsInner_self_eq_normSq
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.hsInner_lerayOpHs_symm
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.hsInner_self_lerayOpHs
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.hsInner_lerayOpHs_sub
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.norm_sq_lerayOpHs_pythagoras
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.lerayOpHs_orthogonal_package
#print axioms TamesisLab.Foundations.LerayOrthogonalSobolev.concrete_lerayOpHs_orthogonal_R3
