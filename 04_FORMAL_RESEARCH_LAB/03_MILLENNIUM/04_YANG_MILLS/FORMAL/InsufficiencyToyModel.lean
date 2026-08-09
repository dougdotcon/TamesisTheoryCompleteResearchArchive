/-
  YM-LIMIT-001 — abstract toy counterexamples supporting the insufficiency
  theorem in `../PROOF_SKETCH.md`.

  STATUS: BUILT (`lake env lean`, exit 0) by the orchestrating session
  during serial integration, outside the original parallel draft step
  (which correctly did not run `lake build` — see AGENTS.md /
  PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md, "condição 3"). Three fixes
  were needed: `hmono_even`/`hmono_odd` used `fun a b h => by omega`
  directly against `StrictMono (fun k => ...)`, and `omega` would not
  beta-reduce the lambda application — rewritten as `by intro a b h;
  simp only; omega`. `toyFiniteVolumeGap` used real division and had to
  be marked `noncomputable`. `#print axioms` on the two main theorems:
  `[propext, Classical.choice, Quot.sound]`, the lab's standard
  footprint. Still NOT registered in `TamesisLab.lean`.

  Every lemma name below was checked BY HAND (via grep against the
  Mathlib snapshot vendored at
  `04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib`,
  toolchain `leanprover/lean4:v4.33.0-rc1`) — not by compiling. Names
  confirmed to exist at the grepped locations:
    - `div_lt_iff₀`            Mathlib/Algebra/Order/GroupWithZero/Basic.lean
    - `exists_nat_gt`          Mathlib/Algebra/Order/Archimedean/Defs.lean
    - `StrictMono.tendsto_atTop` Mathlib/Order/Filter/AtTopBot/Tendsto.lean
    - `tendsto_const_nhds`     Mathlib/Topology/Neighborhoods.lean
    - `tendsto_nhds_unique`    Mathlib/Topology/Separation/Hausdorff.lean
  No incomplete proof, no unjustified premise. If any name has drifted in
  a newer Mathlib pin at integration time, the fix is a name update, not a
  proof gap — the mathematical content (elementary real analysis) is not
  in question.

  Scope: these are ABSTRACT toy models, not a formalization of Yang-Mills
  lattice measures, Hamiltonians, or spectra. They formalize only the
  *logical structure* of the insuffiency argument described in
  `../PROOF_SKETCH.md` and `../COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md`
  (counterexamples 1 and 2 there; counterexample 3, the spectral
  multiplication-operator example, is NOT formalized here — see that file
  for why).
-/
import Mathlib

open Filter Topology

namespace YMLimit001.Toy

/-! ### Counterexample 1
Uniform gap (`∀ n, a n ≥ 2`) does not imply a unique continuum limit:
the even and odd subsequences of `toyGap` converge to different reals. -/

/-- Toy "finite-volume gap" sequence with a uniform positive lower bound,
but no limit: even indices sit at `2`, odd indices sit at `3`. -/
def toyGap (n : ℕ) : ℝ := if n % 2 = 0 then 2 else 3

/-- The gap is uniform: bounded below by `2 > 0` at every stage, the
strongest possible reading of hypothesis `(H_gap)`. -/
theorem toyGap_uniform_lower_bound : ∀ n : ℕ, (2 : ℝ) ≤ toyGap n := by
  intro n
  unfold toyGap
  split <;> norm_num

/-- The even subsequence is constantly `2`, hence tends to `2`. -/
theorem toyGap_even_subseq :
    Tendsto (fun k => toyGap (2 * k)) atTop (𝓝 (2 : ℝ)) := by
  have heq : (fun k => toyGap (2 * k)) = fun _ : ℕ => (2 : ℝ) := by
    funext k
    have h : (2 * k) % 2 = 0 := by omega
    simp [toyGap, h]
  rw [heq]
  exact tendsto_const_nhds

/-- The odd subsequence is constantly `3`, hence tends to `3`. -/
theorem toyGap_odd_subseq :
    Tendsto (fun k => toyGap (2 * k + 1)) atTop (𝓝 (3 : ℝ)) := by
  have heq : (fun k => toyGap (2 * k + 1)) = fun _ : ℕ => (3 : ℝ) := by
    funext k
    have h : (2 * k + 1) % 2 = 1 := by omega
    simp [toyGap, h]
  rw [heq]
  exact tendsto_const_nhds

/-- **Insufficiency, part 1.** A uniform positive gap at every finite
stage (`toyGap_uniform_lower_bound`) does not imply the existence of a
unique continuum limit. This is the exact abstract shape of the
`stop_condition` for YM-LIMIT-001: tightness (here, trivially, boundedness
of a real sequence) only gives a convergent SUBSEQUENCE (Bolzano–
Weierstrass / Prokhorov), never uniqueness of the limit theory. -/
theorem toyGap_no_unique_continuum_limit :
    ¬ ∃ L : ℝ, Tendsto toyGap atTop (𝓝 L) := by
  rintro ⟨L, hL⟩
  have hmono_even : StrictMono (fun k : ℕ => 2 * k) := by
    intro a b h; simp only; omega
  have hmono_odd : StrictMono (fun k : ℕ => 2 * k + 1) := by
    intro a b h; simp only; omega
  have h2 : Tendsto (fun k => toyGap (2 * k)) atTop (𝓝 L) :=
    hL.comp hmono_even.tendsto_atTop
  have h3 : Tendsto (fun k => toyGap (2 * k + 1)) atTop (𝓝 L) :=
    hL.comp hmono_odd.tendsto_atTop
  have hL2 : L = 2 := tendsto_nhds_unique h2 toyGap_even_subseq
  have hL3 : L = 3 := tendsto_nhds_unique h3 toyGap_odd_subseq
  have : (2 : ℝ) = 3 := hL2.symm.trans hL3
  norm_num at this

/-! ### Counterexample 2
Positivity of the gap at every finite stage (`∀ n, g n > 0`) does not
imply a uniform lower bound — i.e. the gap can fail to survive a naive
limit even though it never vanishes at any finite `n`. -/

/-- Toy "finite-volume gap" sequence, positive everywhere, shrinking to
zero: `g n = 1 / (n + 1)`. -/
noncomputable def toyFiniteVolumeGap (n : ℕ) : ℝ := 1 / (n + 1)

/-- The gap is strictly positive at every finite stage. -/
theorem toyFiniteVolumeGap_pos : ∀ n : ℕ, 0 < toyFiniteVolumeGap n := by
  intro n
  unfold toyFiniteVolumeGap
  positivity

/-- The gap is not uniform: for every claimed uniform threshold `ε > 0`
there is a finite stage `n` at which the gap already drops below it. -/
theorem toyFiniteVolumeGap_not_uniform :
    ∀ ε : ℝ, 0 < ε → ∃ n : ℕ, toyFiniteVolumeGap n < ε := by
  intro ε hε
  obtain ⟨n, hn⟩ := exists_nat_gt (1 / ε)
  refine ⟨n, ?_⟩
  unfold toyFiniteVolumeGap
  rw [div_lt_iff₀ (by positivity : (0 : ℝ) < (n : ℝ) + 1)]
  rw [div_lt_iff₀ hε] at hn
  nlinarith

/-- **Insufficiency, part 2.** Positivity of the finite-volume gap at
every `n` (`toyFiniteVolumeGap_pos`) is logically weaker than uniformity
(`∃ c > 0, ∀ n, c ≤ g n`) — the latter fails here
(`toyFiniteVolumeGap_not_uniform`). This is the abstract shape of
`YM-GAP-002` in `../GAP_REGISTER.yaml`: "gap finito-volume não implica gap
uniforme no limite." -/
theorem finite_volume_gap_does_not_survive_without_uniform_bound :
    (∀ n : ℕ, 0 < toyFiniteVolumeGap n) ∧
      ¬ ∃ c : ℝ, 0 < c ∧ ∀ n : ℕ, c ≤ toyFiniteVolumeGap n := by
  refine ⟨toyFiniteVolumeGap_pos, ?_⟩
  rintro ⟨c, hc, hbound⟩
  obtain ⟨n, hn⟩ := toyFiniteVolumeGap_not_uniform c hc
  exact absurd (hbound n) (not_le.mpr hn)

end YMLimit001.Toy
