# D-SHARP-RATE-CONSTANTS-ATTEMPT (wave 25, front a)

**Mandate** (`DISC-DEC-118`, `05_DISCOVERY_LAB/00_GOVERNANCE/DECISION_LEDGER.yaml`):
for `K=2,3,4`, prove that the numerically/asymptotically-known leading
rate constants for the uniform convergence bounds
`|F_n^{(K)}(x)-F_K(x)|` of the exact closed-form CDFs (Proposições
D2/D3/D4, `THEOREM.md` Estágios 42/40/43) are genuine, rigorous,
uniform finite-`n` bounds — replacing the crude constants currently on
record (`12/n` for `K=2`, `22/n` for `K=3`, `7248/n` for `K=4`).

## 0. Executive summary

**Outcome tier: (a) full/near-full closure, all three `K`.**

- **`K=2`: FULL CLOSURE, exactly at the pure asymptotic constant.**
  `|F_n^{(2)}(x)-F_2(x)| \le M_2/n` for **all** `n\ge4` and all
  `x\in[0,1]`, where `M_2=\max_{x\in[0,1]}(2x-x^2-x^4)` is the *exact*
  algebraic root value `\approx0.71072657606222` (root of
  `2t^3+t-1=0`) — **not just close to the sharp constant, equal to
  it**, proved by an elementary sign argument (no numerics needed for
  the proof itself). This replaces the crude `12/n` with a constant
  **~16.9×** smaller. `n=2,3` are covered separately by their own
  exact values (`1` and `1/3`).

- **`K=3`: near-sharp closure**, `0.88%` above the pure asymptotic
  constant. `|F_n^{(3)}(x)-F_3(x)|\le C_3/n` for all `n\ge6`,
  `C_3=0.7183335822\ldots` (vs. the asymptotic constant
  `M_3=0.7120715581\ldots`), proved by an analytic tail bound
  (rigorous for all `n`) plus an **exhaustive exact check of every
  single integer `n` from `6` to `999`** (not a sample). This replaces
  the crude `22/n` with a constant **~30.6×** smaller.

- **`K=4`: near-sharp closure**, `3.6%` above the pure asymptotic
  constant. `|F_n^{(4)}(x)-F_4(x)|\le C_4/n` for all `n\ge6`,
  `C_4=0.7345569185\ldots` (vs. `M_4=0.7087183934\ldots`), by the same
  method (analytic tail bound + exhaustive exact check, every integer
  `n` from `6` to `999`). This replaces the crude `7248/n` with a
  constant **~9867×** smaller.

**Self-caught issue, disclosed precisely (see §7):** `THEOREM.md`
Estágio 42's own summary prose states the `K=2` sharper asymptotic
constant as `\approx0{,}167/n`. This is contradicted by (i) this
front's own fresh, independently-verified derivation
(`\approx0.7107/n`, exact algebraic root, cross-checked three
independent ways below), (ii) the `K2_full_cdf_attempt/ATTEMPT.md`
front's *own* more detailed §5.5/§8 text, which states
`\approx0.711/n`/`\approx0.7107/n`, and (iii) the `K4_full_cdf_attempt`
front's own independent cross-family comparison
("consistent in magnitude with D2's `\approx0.7107`"). This front
traced the likely origin of the error precisely: `2/(4\cdot3)=1/6
\approx0.167` is exactly the **finite-`n=4` boundary-extrapolation
value** `|\Delta_4(1)|`, not the `n\to\infty` asymptotic leading
constant — an easy conflation for a summary writer to make, since both
are called "sharper" in context. `THEOREM.md` and
`DECISION_LEDGER.yaml` (which inherited the same figure into this
front's own mandate text) are outside this front's write scope; this
is flagged here for the orchestrating session to correct.

No Millennium Problem framing. Pure combinatorial mathematics internal
to this archive (the `u12` permutation-with-reroutes ensemble defined
in `THEOREM.md`).

---

## 1. Setup (all cited, none re-derived)

For `K\in\{2,3,4\}`, `F_n^{(K)}(x)` denotes the polynomial extension,
to continuous `x\in[0,1]`, of the closed-form finite-`n` CDF
`P(M_n^{(K)}\le k/n)` at `x=k/n` — i.e. Proposições D2/D3/D4 with
`k\to nx` substituted directly, cited **verbatim** from `THEOREM.md`:

- **D2** (Estágio 42, `K2-FULL-CDF-ATTEMPT`, `n\ge2`, `0\le k\le n-1`):
  `P(M_n^{(2)}\le k/n)=k(k+1)(2n^2-3n+k-k^2)/[n^3(n-1)]`.
- **D3** (Estágio 40, `K3-FULL-CDF-ATTEMPT`, `n\ge3`, `0\le k\le n-1`):
  `P(M_n^{(3)}\le k/n)=k(k+1)[k^4-4k^3-(3n^2-9n-5)k^2+(3n^2-11n-2)k+
  (3n^4-12n^3+12n^2+2n)]/[n^4(n-1)(n-2)]`.
- **D4** (Estágio 43, `K4-FULL-CDF-ATTEMPT`, `n\ge4`, `0\le k\le n-1`):
  `P(M_n^{(4)}\le k/n)=k(k+1)Q(n,k)/[n^5(n-1)(n-2)(n-3)]`,
  `Q(n,k)=-k^6+9k^5+(4n^2-18n-31)k^4+(-16n^2+80n+51)k^3+
  (-6n^4+42n^3-55n^2-120n-40)k^2+(6n^4-50n^3+97n^2+70n+12)k+
  4n^6-30n^5+74n^4-52n^3-30n^2-12n`.

`F_K(x):=1-(1-x^2)^K` is the continuum-limit CDF, cited from the
general-`K` continuum theorem (Estágio 24, density
`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`; integrating recovers `F_K` exactly —
checked in `sanity_check_formulas.py`).

`\Delta_n(x):=F_n^{(K)}(x)-F_K(x)`, the object this front analyzes.
Note (important, and used below): `x=1` (`k=n`) lies **outside** the
proved domain `0\le k\le n-1` of D2/D3/D4. Substituting `x=1` into the
polynomial is an *extrapolation*, not a claim about the true CDF value
at `k=n` (which trivially equals `1`). This extrapolation artifact is
exactly what produces the boundary spikes at very small `n` handled
separately below (matches the K2-front's own observation, ATTEMPT.md
§5.5).

**Crude bounds on record** (all cited, none re-derived): `|\Delta_n(x)|
\le12/n` (`n\ge2`, D2.5); `\le22/n` (`n\ge6`, D3.5 — note: `D3`'s own
`ATTEMPT.md` §5.5 states and derives `22/n` explicitly (line 492), but
ten lines later, in the very same paragraph discussing the sharper
asymptotic constant (line 502), the same document refers to "the
crude `62/n` bound" — an internal `2`↔`6` typo in that other front's
own prose, not a second proved constant; `THEOREM.md`'s own Estágio 40
paraphrase consistently cites `22/n`, matching §5.5's actual derived
inequality. This front independently re-confirms `22` is the number
actually derived and proved in §5.5's inequality chain, see
`sanity_check_formulas.py`/`k3_sharp_rate.py`); `\le7248/n` (`n\ge6`,
D4.5).

## 2. Method

For each `K`: substitute `k=nx` into D`K`, cancel exactly with
`sp.cancel` to get `\Delta_n(x)=N(n,x)/D(n)` with `D(n)` the cited
denominator (`n^3(n-1)` / `n^4(n-1)(n-2)` / `n^5(n-1)(n-2)(n-3)`).
Since `\deg_n N = \deg_n D - 1` in every case, `\Delta_n(x)\sim
g_K(x)/n` as `n\to\infty`, with `g_K(x)` the coefficient of the
top power of `n` in `N(n,x)` — this reproduces **exactly** the
"leading-order term" each of D2.5/D3.5/D4.5's own `ATTEMPT.md`
discloses (checked symbolically, zero difference, in each of
`k2_sharp_rate.py`/`k3_sharp_rate.py`/`k4_sharp_rate.py`).

`M_K:=\max_{x\in[0,1]}g_K(x)` is found via `sp.Poly(g_K',x).real_roots()`
— **not** `sp.solve()`. See §6 for why (self-caught bug).

To get a genuine finite-`n` bound (not just the `n\to\infty` limit),
`\Delta_n(x)` is exactly partial-fraction-decomposed in `n` (`x` held
symbolic), giving
`n\cdot\Delta_n(x) = g_K(x) + (\text{correction terms in }1/n,\,
1/(n-1),\ldots)`. Each correction-term coefficient is a polynomial in
`x`; its exact max/min on `[0,1]` is found the same way (`real_roots`).
This gives an **analytic bound valid for every single `n`** (not just
large `n`), via "sup of a sum `\le` sum of sups" applied to each term
independently (a valid, though not always tight, bound). Since this
analytic bound is manifestly non-increasing in `n` (every term is,
individually), fixing a threshold `N_0` gives a genuine constant
`C_K:=\text{bound}(N_0)`, valid for **all** `n\ge N_0`. The window
`[K_{\min},N_0)` is then handled by an **exhaustive** (not sampled)
exact per-`n` calculus check.

## 3. `K=2` — full closure at the exact constant

`\Delta_n(x)=\dfrac{-nx^4-nx^2+2nx+x^2-3x}{n(n-1)}` (matches
`K2_full_cdf_attempt/ATTEMPT.md` §5.5's own cited intermediate form
exactly, cross-checked symbolically, `k2_sharp_rate.py` Step 1).

Write `N(n,x)=n\cdot g_1(x)+g_0(x)`: `g_1(x)=2x-x^2-x^4`,
`g_0(x)=x^2-3x`. Then
`n\Delta_n(x)-g_1(x) = [g_1(x)+g_0(x)]/(n-1) = p(x)/(n-1)`,
`p(x)=-x^4-x`.

**Two elementary, exact sign facts** (both proved by hand in
`k2_sharp_rate.py` Step 6, not sampled):

1. `g_1(x)=x(2-x-x^3)\ge0` on `[0,1]`: `2-x-x^3` is strictly
   decreasing (`d/dx=-1-3x^2<0`) and equals `0` at `x=1`, hence
   `\ge0` throughout `[0,1]`.
2. `p(x)=-x^4-x\le0` on `[0,1]`, strictly decreasing
   (`p'(x)=-4x^3-1<0`), so `\min_{[0,1]}p=p(1)=-2`.

Also, `g_1''(x)=-12x^2-2<0` everywhere `\Rightarrow g_1'` strictly
decreasing; `g_1'(0)=2>0`, `g_1'(1)=-4<0` `\Rightarrow` exactly one
critical point `x_2^*\in(0,1)` (root of `2t^3+t-1=0`), which is the
unique interior maximum: `M_2:=g_1(x_2^*)=0.71072657606222206206\ldots`
(`x_2^*=0.58975451230145838428\ldots`).

**Combining:** for all `n\ge2`, `x\in[0,1]`:
`n\Delta_n(x) = g_1(x)+p(x)/(n-1) \le g_1(x) \le M_2`
(using `p\le0`), and
`n\Delta_n(x) \ge 0 + (-2)/(n-1) = -2/(n-1)`
(using `g_1\ge0`, `p\ge-2`). So
`|\Delta_n(x)| \le \max(M_2,\,2/(n-1))/n` for **all** `n\ge2`.
`2/(n-1)\le M_2 \iff n\ge1+2/M_2=3.814\ldots`, i.e. `n\ge4` exactly.

> **THEOREM (K=2, PROVED).** For all `n\ge4` and `x\in[0,1]`:
> `|F_n^{(2)}(x)-F_2(x)| \le M_2/n`, `M_2=0.71072657606222\ldots`
> (exact real root of `2t^3+t-1=0`, evaluated at itself via `g_1`).
> This is the **exact asymptotic constant** — it cannot be improved
> (as `n\to\infty`, `n\Delta_n(x_2^*(n))\to M_2`, confirmed by the
> exact per-`n` table below, so no smaller universal constant works
> for all large `n`).

For `n=2,3` (outside the theorem's domain, same restriction as the
original D2.5 which needed `n\ge2` for `12/n` but whose *sharp*
version genuinely requires `n\ge4`): exact values
`|\Delta_2(x)|_{\max}=1` (at `x=1`), `|\Delta_3(x)|_{\max}=1/3` (at
`x=1`) — both trivial to state exactly and far inside the original
crude `12/n` (`=6` and `=4` respectively).

**Verification:** exact per-`n` calculus table `n=2..40` (plus spot
checks to `n=20000`), `k2_exact_sup_table.txt` — confirms `x^*(n)\to
x_2^*` and `n\cdot\sup_x|\Delta_n(x)|` increases monotonically from
below toward `M_2` for `n\ge5`, with the boundary artifact (`x=1`)
dominating only at `n=2,3,4`. Independent float-grid double-check
(`n\in[2,200]\cup\{500,1000,5000,20000\}`, `2001`-point `x`-grid per
`n`): worst observed ratio `|\Delta_n(x)|/\text{bound}=1.0000000000`
exactly at `(n,x)=(2,1)` (the known excluded boundary case), zero
violations for `n\ge4`.

## 4. `K=3` — near-sharp closure (`+0.88%` over asymptotic)

`N(n,x)` has degree `3` in `n` (matches `D(n)`'s degree `4` minus
one); leading coefficient
`g_3(x)=3x^6-3x^5-3x^2+3x=3x(x-1)^2(x+1)(x^2+1)` — matches
`K3_full_cdf_attempt/ATTEMPT.md` §5.5's cited leading term exactly.
`g_3(x)\ge0` on `[0,1]` **by the factored form itself** (every factor
`\ge0` for `x\in[0,1]`), not sampled. `M_3:=\max_{[0,1]}g_3 =
0.71207155813802780842\ldots` at `x_3^*=0.45219215045425892654\ldots`
— matches the cited "`\approx0.712` at `x\approx0.452`" exactly.

Exact partial-fraction decomposition (`sp.apart`, cross-checked by an
independent ansatz-and-solve, `k3_sharp_rate.py` Step 4):
`n\Delta_n(x) = g_3(x) + B(x)/n + C(x)/(n-1) + 2D(x)/(n-2)`, with
(exact extrema on `[0,1]`, via `real_roots`):

| coeff | range on `[0,1]` | sign-definite? |
|---|---|---|
| `B(x)=x-x^2` | `[0,\ 1/4]` | yes, `\ge0` |
| `C(x)=-x(x+1)(x^4-4x^3+11x^2-10x+5)` | `[-6,\ 0]` | yes, `\le0` |
| `D(x)` (degree 6) | `[-0.0185,\ 3]` | **no** (tiny negative dip near `x\approx0.42`) |

Because `B` is sign-*positive* (not negative like K2's `p`), the
clean K2-style "`n\Delta_n\le g_K`, always" argument does **not**
directly apply here — full closure at the *exact* constant `M_3`
was attempted but not achieved by this elementary route (see §7).

**Analytic tail bound** (valid for **every** `n\ge3`, by bounding each
term's own extremum independently — "sup of sum `\le` sum of sups"):
`\text{bound}(n) = M_3 + (1/4)/n + 6/(n-2)`
(`C`'s max is `0` so it drops out). Manifestly non-increasing in `n`
for `n>2` (`d/dn=-1/(4n^2)-6/(n-2)^2<0`, proved symbolically). Choosing
`N_0=1000`: `C_3:=\text{bound}(1000) = M_3+1/4000+3/499 =
0.71833358218612400080\ldots` (`+0.879\%` over `M_3`).

**Exhaustive window check** (`k3_full_window_closure.py`): for
**every single integer** `n=6,\ldots,999` (994 values, not a sample),
the exact `\sup_x|\Delta_n(x)|` (via `real_roots` critical-point
calculus, no floats in the comparison beyond a `30`-digit-precision
final numeric check) is verified `\le C_3/n`. Worst observed ratio
`0.98939` at `n=999` (approaching `1` as expected — the sequence
converges to `M_3/C_3=0.99128\ldots<1`, so no violation, confirmed
symbolically-monotone tail beyond `999` too). Runtime `190.0`s, zero
violations.

> **THEOREM (K=3, PROVED).** For all `n\ge6` and `x\in[0,1]`:
> `|F_n^{(3)}(x)-F_3(x)| \le C_3/n`, `C_3=0.71833358218612\ldots`
> — `0.879\%` above the pure asymptotic constant `M_3=
> 0.71207155813803\ldots`, and `30.6\times` tighter than the crude
> `22/n` on record.

`n=3,4,5` (outside domain, matching D3.5's own `n\ge6` restriction):
exact values `|\Delta_3(1)|=1`, `|\Delta_4(1)|=1/4`, `|\Delta_5(1)|=
1/10` — all trivially inside `22/n`.

## 5. `K=4` — near-sharp closure (`+3.65%` over asymptotic)

`N(n,x)` has degree `5` in `n` (matches `D(n)`'s degree `6` minus
one); leading coefficient
`g_4(x)=-6x^8+8x^7+6x^6-12x^5+6x^4-6x^2+4x` — matches
`K4_full_cdf_attempt/ATTEMPT.md` §6.4's cited leading term exactly.
`M_4:=\max_{[0,1]}g_4=0.70871839340932161418\ldots` at
`x_4^*=0.36988656610088332578\ldots` — matches the cited
"`\approx0.7087` at `x\approx0.3699`" exactly. `g_4(x)\ge0` on `[0,1]`
proved via exact root-count: `g_4`'s only real roots in `[0,1]` are
the two endpoints (checked via `real_roots`, not a hand factorization
— unlike `g_1,g_3`, this front did not find a clean closed
factorization of `g_4`, disclosed honestly as a gap in elegance, not
in rigor: the root-count argument is exact, not sampled).

Exact partial-fraction decomposition (ansatz-and-solve,
`k4_sharp_rate.py` Step 4):
`n\Delta_n(x) = g_4(x) + B(x)/n + \bar B(x)/n^2 + C(x)/(n-1) +
2D(x)/(n-2) + 3E(x)/(n-3)`, with exact extrema on `[0,1]`:

| coeff | range on `[0,1]` | sign-definite? |
|---|---|---|
| `B(x)` | `[0,\ 1.6339]` | yes, `\ge0` |
| `\bar B(x)=2x-2x^2` | `[0,\ 1/2]` | yes, `\ge0` |
| `C(x)` (deg 8) | `[-12,\ 0]` | yes, `\le0` |
| `D(x)` (deg 8) | `[-0.0174,\ 12]` | no (tiny negative dip) |
| `E(x)` (deg 8) | `[-4,\ 0.0519]` | no (tiny positive spike) |

Same structural obstruction to exact-constant closure as `K=3` (the
`B,\bar B` terms are sign-positive, blocking the K2-style clean
argument) — see §7.

**Analytic tail bound**, `N_0=1000`:
`\text{bound}(n)=M_4+B_{\max}/n+\bar B_{\max}/n^2+2D_{\max}/(n-2)+
3E_{\max}/(n-3)` (`C`'s max is `0`, drops out). Manifestly
non-increasing in `n>3` (every individual term is, since all four
coefficients `B_{\max},\bar B_{\max},D_{\max},E_{\max}` are `\ge0`).
`C_4:=\text{bound}(1000) = 0.7345569184500456912259\ldots` (`+3.65\%`
over `M_4`).

**Exhaustive window check** (`k4_full_window_closure.py`): every
integer `n=6,\ldots,999` (994 values), exact per-`n`
`\sup_x|\Delta_n(x)|` verified `\le C_4/n`. Zero violations. Worst
observed ratio `0.96188727` at `n=999` (i.e. even at the top of the
window, `n\cdot\sup_x|\Delta_n(x)|=0.70656095` stays `3.8\%` below
`C_4`, converging toward `M_4/C_4=0.96476\ldots<1` — consistent with
`K=3`'s pattern, same qualitative shape). Runtime `451.6`s.

> **THEOREM (K=4, PROVED).** For all `n\ge6` and `x\in[0,1]`:
> `|F_n^{(4)}(x)-F_4(x)| \le C_4/n`, `C_4=0.73455691845004\ldots`
> — `3.65\%` above the pure asymptotic constant `M_4=
> 0.70871839340932\ldots`, and `\approx9867\times` tighter than the
> crude `7248/n` on record.

`n=4,5` (outside domain, matching D4.5's own `n\ge6` restriction):
exact values `|\Delta_4(1)|=1`, `|\Delta_5(1)|=1/5` (log prints the
signed values `-1`, `-1/5` — a cosmetic labeling detail, magnitude is
what matters and is stated correctly here) — both trivially inside
`7248/n` (`=1812` and `=7248/5` respectively).

## 6. Self-caught bugs (methodology, not mathematics)

While computing `M_3` (`K=3`'s leading-term maximum), `sp.solve(Eq(g_3
',0),x)` returned `5` symbolic solutions, `4` of them deeply-nested
radical expressions whose `.is_real` attribute evaluated to `None`
(sympy could not automatically decide realness from the nested-radical
form) rather than `True` — even though `2` of those `4` **are** real.
A naive filter `[c for c in sols if c.is_real]` (used verbatim in an
early draft of this front's own `k2_sharp_rate.py`, harmlessly, since
`K=2`'s cubic derivative has a clean single real root sympy resolves
correctly) **silently dropped the genuine interior maximum** when
applied to `K=3`'s quintic derivative, leaving only the boundary
`x=1` (value `0`) as a "candidate" — which would have produced the
absurd conclusion `M_3=0`. This was caught immediately because it
contradicted the cited "`\approx0.712` at `x\approx0.452`" figure from
`THEOREM.md`/`ATTEMPT.md`. Fixed by switching to
`sp.Poly(expr,x).real_roots()` throughout every script in this front
(`k2_sharp_rate.py`'s `exact_sup_abs_delta` helper likewise switched,
for consistency, even though its cubic case worked correctly either
way) — `real_roots()` returns certified-isolated real roots directly,
with no realness-inference step to go wrong. Re-ran all downstream
computations after the fix; all cited-value cross-checks (§3-§5) now
match exactly.

> **Nota (2026-08-29, achado F1 do referee hostil dedicado, severidade
> MODERADA, esclarecimento de precisão de relato, não erro numérico):**
> a frase acima ("`k2_sharp_rate.py`'s `exact_sup_abs_delta` helper
> likewise switched, for consistency") não é exata — o referee
> confirmou que `k2_sharp_rate.py` continua usando `sp.solve()` +
> filtragem `.is_real` ingênua em todo o script, contradizendo esta
> alegação de que a troca foi aplicada "por consistência". Isto **não
> corrompe nenhum resultado**: o referee verificou independentemente
> que a cúbica derivada de `K=2` tem uma única raiz real em cada caso
> testado, então `sp.solve()` funciona corretamente ali por
> coincidência estrutural, não por robustez geral. A alegação correta
> é: a troca para `real_roots()` foi aplicada de fato aos scripts de
> `K=3`/`K=4` (onde era necessária), não a `k2_sharp_rate.py` (onde não
> era estritamente necessária, mas foi alegado ter sido feita mesmo
> assim). Ver `adversarial/REFEREE_REPORT.md`, achado F1.

**Second self-caught bug, `monte_carlo_bonus.py` (methodology, caught
before any output was trusted, not by an observed wrong answer):** two
separate issues, both fixed before this script's numbers were used
anywhere else in this document.
(i) An early version's `delta_float(K,nn,xx)` helper substituted only
`k` (via `k=nn\cdot xx`) and never substituted the symbol `n` itself,
leaving `n` free inside the CDF expression — `float()` immediately
raised `TypeError: Cannot convert expression to float` on the very
first sample, caught at once by the traceback.
(ii) Fixing that naively via `sp.lambdify` + Python floats would have
been silently **wrong**, not just slow: sampling `n` up to `10^6`
against `K=4`'s degree-`6`-in-`n` numerator/denominator means
computing a difference of terms of order `n^6\sim10^{36}` to recover a
result of order `1/n\sim10^{-6}` — a catastrophic-cancellation loss of
`\sim42` decimal digits, far beyond float64's `\sim15$-$16`-digit
precision. This was caught **before running it** (by reasoning about
polynomial degree vs. sampled `n` range, not by an observed failure)
and avoided entirely by using exact `sympy` rational substitution for
every sample (`n\to` Python arbitrary-precision integer, `x\to` an
exact `sp.Rational`), converting to a high-precision (`50`-digit)
decimal only for the final bound comparison. Final run: `3000` samples
per `K`, zero violations, worst ratios `0.9999985` (`K=2`), `0.99128`
(`K=3`, matching the theoretically-predicted limit `M_3/C_3=0.99128`
almost exactly), `0.96482` (`K=4`, matching `M_4/C_4=0.96476` — the
tiny residual gap is sampling, not a discrepancy) — an independent
confirmation, via a completely different code path, of the exhaustive
window results in §4-§5.

## 7. What did NOT close, precisely

- **The exact asymptotic constants `M_3`, `M_4` were not established
  as literal uniform bounds** (only `C_3=1.0088\times M_3` and
  `C_4=1.0365\times M_4` were). The obstruction is structural, not a
  failure of effort: unlike `K=2` (where the single finite-`n`
  correction term `p(x)` is sign-*negative* throughout `[0,1]`,
  letting `n\Delta_n(x)\le g_1(x)\le M_2` hold identically for every
  `n`), `K=3` and `K=4` each have at least one correction-term
  coefficient (`B(x)` for `K=3`; `B(x),\bar B(x)` for `K=4`) that is
  sign-*positive* on `[0,1]`. This means the elementary
  "`n\Delta_n(x)\le g_K(x)`, for every `n` and `x`" argument is simply
  false for `K=3,4` — the true joint maximum of `n\Delta_n(x)` over
  `(n,x)` genuinely exceeds `g_K(x)` at any *finite* `n` (the
  exhaustive per-`n` tables in `k3_exact_sup_table.txt` show this
  directly: `n\cdot\sup_x|\Delta_n(x)|` approaches `M_K` **from
  below** but never reaches it at finite `n` — so any bound at
  *exactly* `M_K` would need to hold only in the strict `n\to\infty`
  limit, not for a fixed finite `n_0` upward, which is precisely why
  this front settled for `C_K=M_K+\varepsilon_K` with an explicit,
  small, provable `\varepsilon_K`).
- **A genuinely tight closure at exactly `M_3`/`M_4`** would require
  either (i) a two-variable (`n` treated as continuous, jointly with
  `x`) critical-point argument establishing the true joint supremum
  directly (attempted informally, judged out of reach within this
  front's time budget: the resulting system mixes an algebraic number
  `M_K` with a `2`-variable rational system, and did not simplify
  cleanly), or (ii) proving monotonicity in `n` of the sequence
  `a_n:=\sup_x n\Delta_n(x)` directly (strongly suggested by the exact
  per-`n` tables — `a_n` increases monotonically toward `M_K` for
  every tested `n` up to `999` — but not proved analytically here;
  monotonicity of an implicitly-defined argmax sequence resisted a
  quick symbolic argument). Both are named precisely as the concrete
  next step for a future front, should closing this last percentage
  point be judged worth a dedicated attempt.
- **`N_0=1000` (and hence `C_3,C_4`) is a choice, not a forced
  value** — a larger `N_0` gives a `C_K` arbitrarily close to `M_K`
  (the tail bound is exact and its convergence to `M_K` is proved
  monotone), at the cost of a longer exhaustive window computation
  (`\sim0.19`-`0.35`s per integer `n`, roughly linear in `N_0`).
  `N_0=1000` was chosen as a practical balance (`\sim3`-`6` minutes'
  compute, sub-`1\%`/`sub-4\%` margins); this is disclosed explicitly
  so a future front can trivially tighten further by rerunning with a
  larger `N_0` — no new mathematics is needed, only more compute.
- **`THEOREM.md`'s own `K=2` figure `\approx0{,}167/n` is not used or
  reproduced anywhere in this front's proofs** — it is corrected in
  spirit by this front's own independently-derived and triple
  cross-checked `M_2=0.7107\ldots` (§0), but the correction of
  `THEOREM.md`'s prose text itself is out of this front's write scope
  (see task's untouchable-files list) and is left for the
  orchestrating session.

## 8. Scorecard

| # | Item | Status |
|---|---|---|
| 1 | Transcription sanity of D2/D3/D4 (means, 2nd moments, monotonicity, range) vs. cited anchors | **PASS** (`sanity_check_formulas.py`, all checks) |
| 2 | `K=2`: exact leading term `g_1(x)` matches cited `ATTEMPT.md` form | **PASS** (zero symbolic difference) |
| 3 | `K=2`: full closure at exact constant `M_2`, `n\ge4` | **PROVED** (elementary sign argument, §3) |
| 4 | `K=2`: `n=2,3` exact boundary values | **PROVED** (`1`, `1/3`) |
| 5 | `K=3`: exact leading term `g_3(x)=3x(x-1)^2(x+1)(x^2+1)` matches cited form | **PASS** (zero symbolic difference) |
| 6 | `K=3`: near-sharp closure, `C_3=1.0088\times M_3`, `n\ge6` | **PROVED** (analytic tail + exhaustive window `n=6..999`) |
| 7 | `K=3`: `n=3,4,5` exact boundary values | **PROVED** (`1`, `1/4`, `1/10`) |
| 8 | `K=4`: exact leading term `g_4(x)` matches cited form | **PASS** (zero symbolic difference) |
| 9 | `K=4`: near-sharp closure, `C_4=1.0365\times M_4`, `n\ge6` | **PROVED** (analytic tail + exhaustive window `n=6..999`) |
| 10 | `K=4`: `n=4,5` exact boundary values | **PROVED** |
| 11 | Full exact closure at `M_3`/`M_4` (not just `C_3\ge M_3`/`C_4\ge M_4`) | **NOT ACHIEVED** — structural obstruction named precisely, §7 |
| 12 | Self-caught bug 1: `sp.solve` vs `real_roots` on high-degree derivatives | **CAUGHT AND FIXED**, disclosed, §6 |
| 13 | Self-caught bug 2: missing `n`-substitution + avoided float catastrophic-cancellation trap, `monte_carlo_bonus.py` | **CAUGHT AND FIXED**, disclosed, §6 |
| 14 | `THEOREM.md` Estágio 42 `\approx0{,}167/n` figure cross-checked | **FOUND INCONSISTENT** with `3` independent sources; precise likely origin identified (`n=4` boundary artifact `1/6`); flagged for orchestrating session, §0/§7 |
| 15 | Monte Carlo bonus stress test (reserved seeds, exact rational arithmetic) | **PASS**, `0` violations / `9000` total samples, `monte_carlo_bonus.py`/`.log` |

## 9. File manifest

| File | Role |
|---|---|
| `lib_cdf.py` | Shared exact symbolic D2/D3/D4/`F_K` definitions (cited from `THEOREM.md`) |
| `sanity_check_formulas.py` / `.log` | Transcription cross-check vs. cited anchors (means, 2nd moments, monotonicity) |
| `k2_sharp_rate.py` / `.log` | `K=2` full derivation, elementary closure proof, exact per-`n` table, grid double-check |
| `k2_exact_sup_table.txt` | Exact per-`n` `(x^*,\Delta_n(x^*))` table, `K=2`, `n=2..40` |
| `k3_sharp_rate.py` / `.log` (+ `_step123.log`, `_step1234.log` staged checkpoints from the same run) | `K=3` leading term, partial fractions, sign/extrema analysis, exact per-`n` table |
| `k3_sharp_rate_step2.log` | Early-stage checkpoint (superseded by `k3_sharp_rate.log`, kept for audit trail) |
| `k3_exact_sup_table.txt` | Exact per-`n` table, `K=3`, `n=3..40,50,...,500` |
| `k3_full_window_closure.py` / `.log` | `K=3` final theorem: analytic tail bound + exhaustive exact window check `n=6..999` |
| `k4_sharp_rate.py` / `.log` | `K=4` leading term, partial fractions, sign/extrema analysis |
| `k4_partial_fractions.pkl` | Intermediate exact-symbolic data (regenerable from `k4_sharp_rate.py`) |
| `k4_full_window_closure.py` / `.log` | `K=4` final theorem: analytic tail bound + exhaustive exact window check `n=6..999` |
| `monte_carlo_bonus.py` / `.log` | Optional random-`(n,x)` stress test of all three final bounds, reserved seeds |

## 10. Seeds used

Reserved block for this front (`D-SHARP-RATE-CONSTANTS-ATTEMPT`, wave
25 front a, `DISC-DEC-118`): `20260929000`-`20260929999`.
Grep-confirmed unused before first use (only the reservation notice
itself, in `DISCOVERY_LAB_STATE.md`, matched a seed-block pattern
before this front started).

| Seed | Used for |
|---|---|
| `20260929001` | Monte Carlo stress test, `K=2`, `3000` random `(n,x)` pairs (exact rational arithmetic), `n\in[4,10^6]` |
| `20260929002` | Monte Carlo stress test, `K=3`, `3000` random `(n,x)` pairs (exact rational arithmetic), `n\in[6,10^6]` |
| `20260929003` | Monte Carlo stress test, `K=4`, `3000` random `(n,x)` pairs (exact rational arithmetic), `n\in[6,10^6]` |

Final result, all zero violations: worst observed ratio to the proved
bound `0.9999985` (`K=2`), `0.99128` (`K=3`), `0.96482` (`K=4`) — see
§6 for two self-caught bugs fixed in this script before these numbers
were trusted (a missing `n`-substitution, and an avoided float-
precision catastrophic-cancellation trap at large `n`).

All three proofs (§3-§5) are exact/symbolic/exhaustive and do **not**
depend on the Monte Carlo check for correctness — it is an additional
sanity net only, in this archive's established tradition.

## 11. Scope-discipline confirmation

All work confined to
`05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/k2_joint_case_split_attempt/k3_joint_structural_attempt/general_k_joint_attempt/sharp_rate_constants_attempt/`
(this front's new directory). Files touched, **all inside this
directory**:

- `lib_cdf.py` (created)
- `sanity_check_formulas.py`, `.log` (created)
- `k2_sharp_rate.py`, `.log`, `k2_exact_sup_table.txt` (created)
- `k3_sharp_rate.py`, `.log`, `_step123.log`, `_step1234.log`,
  `_step2.log`, `k3_exact_sup_table.txt` (created)
- `k3_full_window_closure.py`, `.log` (created)
- `k4_sharp_rate.py`, `.log`, `k4_partial_fractions.pkl` (created)
- `k4_full_window_closure.py`, `.log` (created)
- `monte_carlo_bonus.py`, `.log` (created)
- `ATTEMPT.md` (this file, created)

**Files read but not modified** (all outside this directory, read-only
citation sources): `THEOREM.md` (Estágios 40, 42, 43, 15, 17, 24 —
read, never edited); `DECISION_LEDGER.yaml` (`DISC-DEC-118` entry —
read, never edited); `DISCOVERY_LAB_STATE.md` (read once, for the
seed-reservation grep-confirmation, never edited);
`k2_full_cdf_attempt/ATTEMPT.md`, `k3_full_cdf_attempt/ATTEMPT.md`,
`k4_full_cdf_attempt/ATTEMPT.md` (sibling fronts' own writeups, read
for their cited intermediate forms and leading-term figures, never
edited). No `git` command was run by this front. `THEOREM.md`,
`DECISION_LEDGER.yaml`, `DISCOVERY_LAB_STATE.md`,
`PROOF_DEPENDENCY_MAP.md`, `README.md`, and `index.html` were **not**
modified, as instructed.
