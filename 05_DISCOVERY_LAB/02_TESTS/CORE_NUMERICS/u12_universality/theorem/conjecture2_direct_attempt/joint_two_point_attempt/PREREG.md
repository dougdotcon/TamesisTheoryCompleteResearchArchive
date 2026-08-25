# Pre-registration — JOINT-TWO-POINT-EXPLORATION-ATTEMPT (wave 17, front (c), DISC-DEC-072)

Written BEFORE any script in this directory ran. Seeds: fresh block
`20260864000+` (grep-confirmed: the only prior occurrence of
"20260864" in the archive is the reservation line in
`DECISION_LEDGER.yaml`, DISC-DEC-072). Referee block `20260865000+`
will NOT be touched by this front.

## Paper derivation completed before this file (to be verified by the scripts below)

A sequential two-walker (and p-walker) exploration of `L(c)` was
derived on paper from Definition 2, using the same lazy-revelation /
gap-closure machinery that Definition 3 + Proposition 2.4 use for one
point. Structural claims to be written up in ATTEMPT.md and tested
here:

1. **(S1, structure)** Conditional on `x₁` cyclic with arc-0 closure at
   explored mass `t`, the entire explored region is exactly the cycle
   of `x₁`, with mass exactly `t`.
2. **(S2, Term 1)** `E[1{x₁ cyc}·mass(cycle(x₁))] = E[Σᵢ mᵢ²]` (sum
   over final cycles) `= ∫₀¹ t(1−t²)^K dt = 1/(2(K+1))` in the K-mark
   model; `= (1−e^{−c})/(2c)` in the Poisson model.
   Hand-verified anchors before any script: `K=0` gives `1/2` (classical
   `PD(1)` fact = Lemma B1 of Estágio 18); `K=1` gives `1/4` by a fully
   independent computation from the proved §5.3 whole-space law
   (branch (a): `(1/2)E[(1−L)³] = 1/8`; branch (b): `E[L(1−L)²]/2 +
   E[L³]/3 = 1/24 + 1/12 = 1/8`; total `1/4`).
3. **(S3, Term 2)** `P(x₁,x₂ cyclic on different cycles)` also equals
   `1/(2(K+1))` (K-model) and `(1−e^{−c})/(2c)` (Poisson), via the
   second walker's era: closure `τ|t ~ dτ/(1−t)` on `(t,1)`, per-mark
   joint success probability exactly `1−τ` for every mark position
   `S<τ` (same cancellation as Theorem 1 Step 4), leftover walker-1
   arcs memoryless with survival `(1−τ)/(1−t)`.
4. **(S4, main targets)** Hence `E[M_K²]=1/(K+1)` for ALL `K`, and
   `E[M(c)²]=(1−e^{−c})/c` — mandate targets (1) and (2). Corollary:
   among both-cyclic pairs, same-cycle and different-cycle
   contributions are EXACTLY equal (50/50).
5. **(S5, general p)** `E[M_K^p] = E[(1−W_p²)^K]` with
   `W_p = max(U₁,…,U_p)` ~ Beta(p,1) (absorption/refresh recursion
   `W_j = max(W_{j−1}, U_j)`); i.e.
   `E[M_K^p] = ∫₀¹ p w^{p−1}(1−w²)^K dw`. Hand-verified anchors before
   any script: `p=1` reproduces Lemma 2 (`φ_K`); `p=2,K≤4` gives
   `1/2,1/3,1/4,1/5`; `p=3,K=3` gives `16/105` and `p=3,K=4` gives
   `128/1155`, both matching Estágios 17/20's recorded third moments;
   `K=1` gives `2/(p+2) = ∫ x^p·2x dx` for all p.
6. **(S6, consequence)** If S5 holds, all moments of `M_K` match
   `2Kx(1−x²)^{K−1}`, and by Hausdorff determinacy (Estágio 18 §2,
   CITED) Conjecture 1 follows for all K, and Conjecture 2 follows by
   Poisson mixture (moments `e^{−c}+γ(p/2+1,c)/c^{p/2}`, matching the
   referee's S9b record).
7. **(S7, refuted shortcut, self-caught)** The naive "per-mark
   factorization on frozen geometry" — `P(both cyc|K) = E[A^K]` with
   `A` the one-mark joint-harmless kernel (`a_same(ℓ,β) = 1−ℓ+ℓ²(β²+(1−β)²)/2`,
   `a_diff(ℓ₁,ℓ₂) = 1−ℓ₁−ℓ₂+(ℓ₁²+ℓ₂²)/2`) — is REFUTED at K=2:
   `E[A²] = 49/180 ≠ 1/3` (both geometry cases give `E[a²]=49/180`;
   `E[A]=1/2` does match K=1). This was this front's own first idea,
   killed on paper before any script.

## Test plan (numbered; scripts to be written after this file)

- **T1 (exact symbolic, sympy):** all integrals/identities in S2–S7 in
  exact arithmetic, symbolic in K and p where feasible; the
  incomplete-gamma moment identity for the conjectured law; the
  Poisson mixtures.
- **T2 (exact enumeration, Fractions):** finite-n conditional-K model
  (uniform permutation of [n]; uniform K-subset rerouted; i.i.d.
  uniform destinations): exact `P(1,2 both cyclic)`, split into
  same-cycle / different-cycle parts, for `n` up to 7 (K=1) and up to
  6–7 (K=2). Expect approach to `1/(K+1)` with `O(1/n)` drift and the
  split ratio → 1/2.
- **T3 (fresh MC, finite-n large):** conditional K ∈ {2,3,5,6}: per
  trial compute cyclic count C and Σ(cycle sizes²); check
  `E[(C/n)²] → 1/(K+1)`, `E[Σm²] → 1/(2(K+1))`, `E[(C/n)³]` vs S5's
  p=3 prediction, and KS of `C/n` against `F(x)=1−(1−x²)^K` at K=5,6
  (instances of Conjecture 1 with NO previously proved density —
  novel-prediction test). Seeds `20260864000+`, all logged.
- **T4 (fresh MC, Poisson model):** c=2 (a value not used by Estágio
  18): `E[M²]` vs `(1−e^{−2})/2`, `E[M³]` vs `e^{−2}+γ(5/2,2)/2^{3/2}`,
  and the 50/50 split.
- **T5 (fresh MC, K=1 kernel):** verify `a_same`, `a_diff` bin-by-bin
  (direct test of the one-mark two-point kernel used in S7's
  refutation).

Failure of any of T2–T5's novel predictions falsifies the
corresponding structural claim and will be reported as such.
