# The u12 reroute-permutation ensemble as an interpolation between permutation cycle statistics and Kolchin's random mappings

**Front:** `U12-EXTERNAL-POSITIONING-ATTEMPT`, `DISC-DEC-096`, wave 22 front
(d). **This is an expository/positioning document, not a mathematics
front.** It makes **no new mathematical claim** of any kind, proves
nothing, and does not extend, re-derive, or weaken any result of this
archive. Every mathematical statement below is either quoted/restated
faithfully from an already-PROVED result of `theorem/THEOREM.md` or one of
its integrated extensions ("Estágios"), or explicitly flagged as
**pending internal review** (the general-`K` front, not yet a catalogued
Estágio). **No claim of progress on any Millennium Prize Problem, or any
other famous unsolved problem, is made anywhere in this document.** This
is a self-contained combinatorics object internal to this archive; nothing
below should be read as touching any problem outside it.

**Purpose.** This note positions the archive's own "reroute-permutation"
ensemble ("Object A" below) explicitly against the two classical
neighboring bodies of literature — permutation cycle statistics (the
`K=0` corner) and V. F. Kolchin's theory of random mappings (the `K=n`
corner) — using notation and framing a specialist in that literature
would recognize, so that such a specialist, if shown this note, can
quickly assess whether Object A and the exact finite-`n` formulas proved
about it constitute a genuinely new, citable contribution.

**On the location of this document.** The archive has one established
convention for packaging a *complete, submission-ready* external result:
`tamesis-cycle-survival/` at the repository root (wave 3, `DISC-DEC-018`
lineage) — a compiled LaTeX paper (PDF), independent clean-room
simulation scripts, and a `.bib` file, built for a single, fully-proved
result (`Theorem 1`'s closed form on `L(c)`) intended as a stand-alone
external submission. That convention was checked and is **not reused
here**: this note is explicitly scoped as an internal positioning/context
document reviewed only by the orchestrating session — not a
submission-ready package, and not something that goes through the
archive's proof-integration/referee pipeline (see `DISC-DEC-096`, front
(d) mandate). It is placed instead at the location the front's own
mandate specifies for this kind of document,
`02_TESTS/CORE_NUMERICS/u12_universality/EXTERNAL_POSITIONING_NOTE.md`,
alongside the object it describes. The `tamesis-cycle-survival/`
`.bib` file's already-verified citation entries (Kingman 1975,
Hansen–Jaworski 2014, Scheffé 1947, Le Cam 1960, Arratia–Barbour–Tavaré
2003, Pitman 2002) are reused verbatim below where they recur; the two
citations specific to this note's framing (Kolchin 1986, Flajolet–Odlyzko
1989/1990) were independently checked against public bibliographic
sources for this document (§7).

---

## 1. Object A: formal definition

Object A is exactly `THEOREM.md`'s Definition 4, restated with its own
supporting Definition 1. Both are quoted here with only cosmetic
rewording of connective prose; no symbol, quantifier, or hypothesis is
altered.

### 1.1 The finite combinatorial object ("Object A" proper)

Let `[n] = \{1,\ldots,n\}`. A **random mapping** is a function `f:[n]\to[n]`
(not necessarily injective); its **functional digraph** has an arc
`i\to f(i)` for every `i`. A point `i` is **cyclic** for `f` iff
`f^t(i)=i` for some integer `t\ge1`, equivalently iff `i` lies on a
directed cycle of the functional digraph. (This is exactly the standard
random-mapping-statistics vocabulary — Kolchin 1986; Flajolet–Odlyzko
1989/1990 — and is already stated in these terms in `THEOREM.md` §0.)

> **Definition (`THEOREM.md` Definition 4, `M_n(c)` conditioned on exactly
> `K` reroutes — "Object A").** Fix `n\in\mathbb N` and an integer
> `0\le K\le n`. Let `\pi` be a uniform random permutation of `[n]`. Fix a
> `K`-element subset `S\subset[n]` of **reroute sources** (by the
> exchangeability established below, which subset is fixed does not
> matter). Let `U_i`, `i\in S`, be i.i.d. `\mathrm{Uniform}([n])`,
> independent of `\pi`. Define the random mapping
>
> `f(i) := U_i` if `i\in S`,  `f(i) := \pi(i)` if `i\notin S`.
>
> Write `\varphi_n^{(K)} := E[\,\#\{i:i\text{ cyclic for }f\}\,]/n` and
> `M_n^{(K)} := \#\{i:i\text{ cyclic for }f\}/n` (so
> `\varphi_n^{(K)}=E[M_n^{(K)}]`). Since `\pi` is independent of the choice
> of `S` and of the `U_i`'s, conditioning on a *uniformly random* `K`-subset
> `S` (equivalently: taking `\pi` uniform, then rerouting a uniform random
> `K`-subset of indices) leaves the law of `M_n^{(K)}` unchanged by
> exchangeability — `\varphi_n^{(K)}` and the full law of `M_n^{(K)}` depend
> only on `(n,K)`, never on which `K`-subset `S` is realized. `M_n^{(K)}` is
> thus a well-defined, purely combinatorial (no continuous parameter) random
> variable.

This is precisely the object described in this front's mandate: "a
uniform random permutation of `[n]` with `K` designated reroute sources
whose images are replaced by i.i.d. `\mathrm{Uniform}([n])` targets
instead of the permutation's own value."

### 1.2 The one-parameter Poissonized ensemble containing it

> **Definition (`THEOREM.md` Definition 1, `M_n(c)`).** Fix `n\in\mathbb N`
> and `c\ge0`. Let `\pi` be a uniform random permutation of `[n]`.
> Independently, for each `i\in[n]` let `\xi_i` be i.i.d. Bernoulli with
> `P(\xi_i=1)=c/n` (for `n>c`; `q=c/n\wedge1` if `n\le c`), and let `U_i`
> be i.i.d. `\mathrm{Uniform}([n])`, independent of `\pi` and of the
> `\xi`'s. Define `f(i)=U_i` if `\xi_i=1`, `f(i)=\pi(i)` if `\xi_i=0`. The
> observable is `\varphi(n,c) := E[\#\{i:i\text{ cyclic for }f\}]/n
> = P(1\text{ is cyclic for }f)` (the second equality by exchangeability).

Writing `K_n:=\#\{i:\xi_i=1\}\sim\mathrm{Binomial}(n,c/n)`, Definition 1
conditioned on `K_n=K` **is** Object A (Definition 4) exactly, and the
exact finite-`n` mixture identity holds unconditionally for every `n>c`
(`THEOREM.md` Fact 4.1):

`\displaystyle \varphi(n,c) = \sum_{K=0}^n\binom nK\Big(\frac cn\Big)^K\Big(1-\frac cn\Big)^{n-K}\varphi_n^{(K)}`.

So Object A (fixed, finite `K`) is the "conditional slice at exactly `K`
reroutes" of the one-parameter ensemble `M_n(c)`; `c` is the ensemble's
mean number of reroutes, `K` a realized, exact count.

### 1.3 The `n\to\infty` continuum limit `L(c)`

`THEOREM.md` also constructs and studies (not required for Object A's own
definition, but part of the same document, quoted here for completeness
since the front's mandate names it) an explicit `n\to\infty` limit object
`L(c)`, in two layers:

> **Definition (`THEOREM.md` Definition 2, canonical form).** `L(c)`
> consists of: (i) a random partition of `[0,1]` (Lebesgue measure) into
> countably many disjoint measurable "cycles," with the multiset of their
> masses distributed as `\mathrm{PD}(1)` (Kingman 1975; the
> size-biased/stick-breaking `\mathrm{GEM}(1)` representation is due to
> McCloskey 1965 and Patil–Taillie 1977; see also Pitman 2002, Ch. 3), a
> marked point `x_0` placed independently and uniformly on `[0,1]`, and
> each block equipped with a cyclic (rotational) order; (ii) independently,
> a Poisson process of rate `c` on `[0,1]` ("marks"), each carrying an
> independent `\mathrm{Uniform}(0,1)` destination; (iii) the mapping: an
> unmarked point moves to the next point on its cycle; a marked point moves
> to its destination instead. A point is **cyclic** iff its forward orbit
> returns to itself in finitely many steps.

> **Definition (`THEOREM.md` Definition 3, explicit construction).** On a
> common probability space: `E_0,E_1,E_2,\ldots` i.i.d. `\mathrm{Exp}(1)`; a
> rate-`c` Poisson process `\mathcal N` on `[0,1)`, `K:=\mathcal
> N([0,1))\sim\mathrm{Poisson}(c)`, points `S_1<\cdots<S_K`;
> `\Theta_1,\ldots,\Theta_K` i.i.d. `\mathrm{Uniform}(0,1)`. Set
> `T_0:=1-e^{-E_0}`. Processing marks `j=1,\ldots,K` in increasing `S_j`
> order while maintaining a set `\mathcal A` of open "arc-heads" with
> closure times `T_i` (initialize `\mathcal A=\{0\}`): stop (no kill) once
> `S_j\ge\min_{i\in\mathcal A}T_i`; declare a **kill** and stop if
> `\Theta_j<S_j`; otherwise set `T_j:=S_j+(1-S_j)(1-e^{-E_j})` and add `j`
> to `\mathcal A`. A kill means `x_0` is **not cyclic**; otherwise, with
> `T^*:=\min_{i\in\mathcal A}T_i` attained at `i^*`, `x_0` is **cyclic iff
> `i^*=0`**. `\varphi_\infty(c):=P(x_0\text{ cyclic})` under this
> construction is the operational meaning of "fraction of cyclic points in
> `L(c)`" used throughout `THEOREM.md`.

`L(c)` is *not itself* Object A — it is the archive's `n\to\infty`,
continuum-limit companion object, related to Object A by the bridge
results summarized in §3.6 below (a bridge that is, itself, only
partially proved — see §4).

---

## 2. Framing: Object A as an interpolation

**The two classical endpoints.**

- **`K=0`.** No point is rerouted; `f=\pi` exactly, a genuine permutation.
  `M_n^{(0)}` is then the classical object of permutation cycle
  statistics: the fraction of points of a uniform random permutation of
  `[n]` lying on a cycle is trivially `1` (every point of a permutation is
  cyclic, `\varphi_n^{(0)}=1` identically), but the underlying cycle-length
  statistics — the object whose `n\to\infty` limit is the
  Poisson–Dirichlet/GEM family — are exactly the classical theory this
  archive cites without re-deriving (Kingman 1975, *Random discrete
  distributions*, J. R. Stat. Soc. B **37**; the Feller-coupling/size-biased
  machinery of Arratia, Barbour & Tavaré, *Logarithmic Combinatorial
  Structures: A Probabilistic Approach*, EMS 2003, Chs. 4–5; Pitman,
  *Combinatorial Stochastic Processes*, École d'Été de Probabilités de
  Saint-Flour XXXII, Springer LNM **1875** (2002), Ch. 3).

- **`K=n`.** Every point is rerouted, so `f(i)=U_i` for **every** `i\in[n]`
  — an elementary, immediate consequence of Definition 4 at `K=n`, not a
  theorem: `f` is by construction a **uniform random mapping** `[n]\to[n]`,
  entirely independent of `\pi` (which plays no role at all once `K=n`).
  This is precisely the classical object of V. F. Kolchin's theory of
  random mappings (*Random Mappings*, Optimization Software, Inc.
  Publications Division, New York, 1986 — an English translation,
  *Translations Series in Mathematics and Engineering*, of *Slučajnye
  Otobraženija*, Nauka, Moscow, 1984) and of Flajolet & Odlyzko's
  generating-function/singularity-analysis treatment ("Random Mapping
  Statistics," in *Advances in Cryptology — EUROCRYPT '89*, Lecture Notes
  in Computer Science vol. 434, Springer, 1990, pp. 329–354; presented at
  EUROCRYPT '89, Houthalen, Belgium) — the number of cyclic points of a
  uniform random self-map of an `n`-set, its expectation
  `\sim\sqrt{\pi n/2}`, and roughly twenty further parameters of the same
  functional-graph model, are exactly their subject.

**Object A (Definition 4, §1.1) is the finite, discrete-`K` interpolation
between these two corners**: at `K=0` it is a bare permutation; at `K=n`
it is Kolchin's uniform random mapping; for `0<K<n` it is a genuine
hybrid — a permutation on `n-K` of its `n` points, corrupted at exactly
`K` independently and uniformly rerouted points. The Poissonized ensemble
`M_n(c)` (§1.2) sits inside this same family, realizing a *random* `K`
via `K_n\sim\mathrm{Binomial}(n,c/n)`.

**What this note can, and cannot, honestly say about that interpolation.**
Every exact and asymptotic result this archive has proved about Object A
(§3 below) lives in the regime **`K` fixed (not scaling with `n`) as
`n\to\infty`**, or fully finite `n` with small fixed `K`
(`K=1,2,3` proved unconditionally; `K=4,5,6` computed and verified but
**pending internal review**, §5) — deep in the "near-permutation" end of
the `K=0,\ldots,n` line. The `K=n` endpoint is reached, in this archive,
only in the elementary sense stated above, **plus** one genuinely exact,
already-integrated identity that is worth flagging here even though it
falls outside this note's required-reading list (`THEOREM.md` "Estágio
10," `theorem/uniform_in_c_attempt/ATTEMPT.md` §7.1, Proposição 7.1 —
verified by this note's author directly against its source, PROVED, with
an elementary one-line proof): setting `c=n` in the Poissonized ensemble
`M_n(c)` forces `q=c/n\wedge1=1`, i.e. `K_n=n` deterministically, and

`\varphi(n,n) = Q(n)/n`,  `Q(n):=\sum_{j\ge0}\prod_{i=1}^j\Big(1-\frac in\Big)`

exactly, where `Q` is Ramanujan's `Q`-function — the same function whose
asymptotics `Q(n)=\sqrt{\pi n/2}-\tfrac13+O(n^{-1/2})` this archive already
cites from Knuth (*TAOCP* I §1.2.11.3) and from Flajolet–Odlyzko
(EUROCRYPT'89) for the **classical, `K`-free** cyclic-point count of a
uniform random mapping. So the `K=n` corner of Object A is connected to
the classical Kolchin/Flajolet–Odlyzko statistic not just definitionally
but via a proved, exact, finite-`n` identity already on record in this
archive.

**What is honestly *not* established, and would be the natural next
question if this framing is pursued further:** the **crossover regime**
— `K` comparable to `n` (e.g. `K=\gamma n` for fixed `\gamma\in(0,1)`, or
any regime where `K\to\infty` together with `n`) is **not analyzed
anywhere in this archive**. Every exact and asymptotic result below holds
for `K` a fixed constant (independent of `n`) as `n\to\infty`. Framing
Object A as "the interpolation between `K=0` and `K=n`" is accurate as a
description of the *family*, but the archive's actual analytic reach
covers only its near-`K=0` end (plus the single, isolated, exact `K=n`
identity above); the middle of the line is an open question this note
does not, and should not, claim any progress on.

---

## 3. Restatement of the archive's proved results

All results below are quoted from `THEOREM.md`'s main text (§§0–7) and
its integrated extensions ("Estágio" `N`, dated addenda, each
independently adversarially refereed — verdicts summarized in §4). Nothing
is re-derived, extended, or altered here; only the presentation is
adapted toward standard functional-graph/cyclic-point vocabulary.

### 3.1 Single-point marginal statistics, fixed `K`

- **`K=0` (trivial, exact for every `n`).** `\varphi_n^{(0)}=1`: a
  permutation's cycles cover `[n]`.
- **`K=1` (Proposition 4, PROVED, exact for every `n\ge1`).**
  `\displaystyle \varphi_n^{(1)} = \frac{2n^2+1}{3n^2} = \frac23+\frac1{3n^2}`.
- **General `K`, the mean of the `n\to\infty` limit (Lemma 2, PROVED — a
  Wallis-integral computation on `L(c)`, §1.3).**
  `\displaystyle \varphi_K = \int_0^1(1-t^2)^K\,dt = \frac{4^K(K!)^2}{(2K+1)!}`
  for every `K\ge0` (`\varphi_0=1,\varphi_1=\tfrac23,\varphi_2=\tfrac8{15},
  \varphi_3=\tfrac{16}{35},\ldots`), and `\varphi_n^{(K)}\to\varphi_K` as
  `n\to\infty` is proved unconditionally for every fixed `K\ge0` — the
  "fixed-`K` bridge" that `THEOREM.md`'s Stage 2 (§7) leaves as an *Open
  Lemma* is fully closed later in the same document's Estágio 6 (all
  `K\ge0` incondicionalmente), promoting the general `M_n(c)\to L(c)`
  mean-convergence to an unconditional theorem (`\varphi(n,c)\to
  \varphi_\infty(c)=\int_0^1e^{-ct^2}dt` for every fixed `c\ge0`).
- **`K=1` full distributional law (Lemma 2 density, PROVED, on `L(c)`).**
  The cyclic-mass fraction `M_1` has density `f_{M_1}(x)=2x` on `(0,1)`.
- **General-`K` density: CONJECTURE, not proved in this archive.**
  `f_{M_K}(x)=2Kx(1-x^2)^{K-1}` on `(0,1)` for `K\ge2` is recorded as a
  conjecture (mean-consistency proved; KS-test support at `K=1,2,3`); it
  is **not derived** from first principles here.

### 3.2 The known match with Hansen–Jaworski's local limit theorem

The `K`-conditional density above (proved at `K=1`, conjectured for
`K\ge2`) coincides — functional form and mean, exactly — with the local
limit theorem for a **structurally different** random-mapping model:

> **Hansen & Jaworski, "Structural transition in random mappings,"
> *Electronic Journal of Combinatorics* **21**(1) (2014), #P1.18.
> Theorem 7(ii).** For `0<x<1` fixed, `r=n-a` with `a\in\mathbb Z^+` fixed,
> `k=\lfloor xn\rfloor`: `\displaystyle P\{\hat X_n^r=k\}\sim\frac1n\,
> 2ax(1-x^2)^{a-1}`.

Their `\hat T_n^r` is drawn *uniformly* from mappings with `r` vertices
constrained to in-degree `\le1` and the rest to in-degree `\le2` — a
model built from a fixed in-degree sequence, with **no permutation +
independent-reroute mechanism at all** — whereas Object A is a uniform
permutation independently corrupted at `K` points. That two
microscopically different constructions produce, conditional on the same
"defect count" `a=K`, the same limiting density is exactly the kind of
fact worth flagging as **evidence for, not proof of**, the `K\ge2`
conjecture above (this is `THEOREM.md`'s own framing, §5.5, unaltered).
This is also, per this archive's own priority search
(`priority_search/PRIORITY_SEARCH.md`, quoted in §6 below), the *origin*
of the `K`-conditional density for the Hansen–Jaworski lineage — a
citation-neighborhood the archive reports as closed (no located successor
of Theorem 7(ii) extends it).

### 3.3 An exact finite-`n` bijective fact: uniform restriction to the eventual cycle set

> **Theorem J (Uniform Cyclic Restriction Theorem; Estágio 25, PROVED,
> elementary and self-contained).** In Object A (`n,K` arbitrary, finite),
> conditional on the realized cyclic point-set `C(f)=c` (any subset with
> `|c|=m\ge2`), the restriction `f|_c` is **exactly uniformly distributed**
> over all `m!` bijections of `c` — for **every** `n,K`, not merely
> asymptotically. (Proof: post-composition invariance under any fixed
> bijection of `[n]`, plus an explicit transposition-exchange bijection
> between the events `\{C(h)=c,h|_c=\rho\}` and `\{C(h)=c,h|_c=\rho'\}`
> whose support is shown, by induction on the pre-`c` orbit tail, never to
> reach outside `c`.)

> **Corollary (Estágio 25, PROVED).**
> `P(\text{two fixed points end up on the same final cycle}\mid\text{both
> cyclic}) = \tfrac12` **exactly**, for every finite `n\ge2` and every
> `0\le K\le n`.

This is a genuine finite-`n` fact about the functional-graph structure of
Object A — the restriction of `f` to its own eventual cycle set is a
Haar-uniform random permutation of that set, independent of `n,K`.

### 3.4 The continuum same-cycle transfer pattern

Combining Theorem J's Corollary (exact at finite `n`, §3.3) with
convergence of the relevant "both query points cyclic" probability
`P_{nn}(n,K)` (§3.5) gives, **by transfer** (an elementary consequence,
not a direct continuum-native construction — see §4 for the precise
distinction the archive itself draws): if `P_n^{(K)}(\text{both
cyclic})\to\tau_K` then automatically `P_n^{(K)}(\text{same
cycle})\to\tau_K/2`. Carried out for `K=0,1` (Estágio 28), `K=2`
(Estágio 31), and `K=3` (Estágio 35):

> `\displaystyle P(\text{two marked points end up on the same final
> cycle}\mid K\text{ reroutes}) \;\longrightarrow\; \frac1{2(K+1)}`
> confirmed exactly for `K=0,1,2,3` (values `\tfrac12,\tfrac14,\tfrac16,
> \tfrac18`), each obtained by a finite-`n` closed form plus its `n\to
> \infty` limit — not asserted for general `K` (see §4).

### 3.5 Exact finite-`n` joint two-point (second-moment) formulas

Writing `P_{nn}(n,K):=P(\text{two points disjoint from all }K\text{
sources both cyclic})` (the scalar Lemma P2, Estágio 27, reduces the
second-moment bridge target `E[(M_n^{(K)})^2]\to1/(K{+}1)` to exactly this
quantity, for general `K`, PROVED as a reduction):

- `K=1`: `P_{nn}(n,1) = \tfrac12+\tfrac1{6n}` (Estágio 27).
- `K=2` (**Proposition NN2**, Estágio 31, PROVED, `n\ge4`):
  `\displaystyle P_{nn}(n,2) = \frac{10n^2+7n+2}{30n^2}
  = \frac13+\frac7{30n}+\frac1{15n^2}`.
- `K=3` (**Proposition NN3**, Estágio 35, PROVED, `n\ge5`, symbolic exact
  derivation): `\displaystyle P_{nn}(n,3) =
  \frac{35n^3+38n^2+23n+6}{140n^3}
  = \frac14+\frac{19}{70n}+\frac{23}{140n^2}+\frac3{70n^3}`.

Each converges to `\tfrac1{K+1}` as `n\to\infty`, consistent with
`E[M_K^2]=1/(K{+}1)` (proved unconditionally for **all** `K` by a
different route entirely — the general-`K` closure of a distributional
conjecture in Estágio 24, outside this note's required-reading scope,
cited here only for context, not restated in detail).

Separately, the **full second moment of the cyclic-mass fraction itself**
(not the disjoint-pair scalar `P_{nn}`) is proved exactly at `K=1`
(Estágio 27, Corollary D1.2): `E[(M_n^{(1)})^2]=\tfrac12+\tfrac1{2n^2}`
— a different, also-exact quantity with the same `n\to\infty` limit
`\tfrac12`; the two are not to be conflated (they differ by which pairs
of points are averaged over: all pairs vs. pairs disjoint from the `K`
sources).

### 3.6 Two elementary lemmas about the "`K` marked sources in a functional graph" structure

Two structural lemmas, proved for `K=3` in Estágio 35 and (in the
pending-review document, §5) shown to generalize to every `K` with the
**same, unmodified proof**:

> **Governing-Source Reindexing (Estágio 35, PROVED at `K=3`; general-`K`
> statement pending review, §5).** For `K` marked sources fixed WLOG in
> a uniform random permutation, the "contracted" permutation `\sigma`
> induced on the `K` sources is uniform on `S_K`, **independently** of the
> vector of arc-lengths `(L_1,\ldots,L_K)` (governing-source-indexed gap
> sizes) — a corollary of the more general **Marked-Point Gap Structure
> Lemma** (Estágio 31, PROVED for general `m`: for `m` marked points in a
> uniform random permutation of `[n]`, the induced contracted permutation
> on the `m` points is uniform on `S_m`, and, independently, the vector of
> gap sizes between consecutive marked points is uniform over compositions
> of `n-m` into `m+1` nonnegative parts).

> **Cycle-Predecessor Uniqueness (Estágio 35's "Lemma 4," PROVED at
> `K=3`; general-`K` statement pending review, §5).** In the induced
> functional digraph on the `K` reroute sources plus one absorbing "dead"
> state (a source's target either lands on another source, on itself, or
> outside all `K` source-arcs), any source `s` that is cyclic has a
> **unique** cycle-predecessor among the `K` sources; any other source
> whose target also happens to land in `s`'s arc is provably inert — it
> never affects which points of that arc end up cyclic. This is an
> elementary fact about **any** finite functional digraph with
> out-degree `1` per node plus one absorbing sink — not specific to `K=3`
> or to permutations at all.

These two lemmas are the mechanism behind §3.5's exact closed forms; they
are elementary consequences of exchangeability and of standard
functional-digraph structure (every node's forward orbit either absorbs
or, by pigeonhole, revisits a node and cycles from there), stated here in
functional-graph language matching the random-mapping-statistics
literature's own vocabulary for such digraphs.

---

## 4. What is and isn't established

| Result | Status | Source |
|---|---|---|
| Definitions 1–4 (Object A, `M_n(c)`, `L(c)`) | Definitional, not a claim | `THEOREM.md` §§1–2, §7.2 |
| `\varphi_n^{(0)}=1`; `\varphi_n^{(1)}=\tfrac23+\tfrac1{3n^2}` | **PROVED**, exact all `n` | `THEOREM.md` §7.3, Proposition 4 |
| `\varphi_K=4^K(K!)^2/(2K{+}1)!`; `\varphi_n^{(K)}\to\varphi_K` for **every** `K\ge0` | **PROVED** (mean; Wallis integral + Poisson-limit reduction) | `THEOREM.md` §5.2, §7 Open Lemma resolved unconditionally, Estágio 6 |
| `f_{M_1}(x)=2x` | **PROVED** (whole-space, `K=1` only) | `THEOREM.md` §5.3 |
| `f_{M_K}(x)=2Kx(1-x^2)^{K-1}`, `K\ge2` | **CONJECTURE** — mean-consistency proved, KS-test and Hansen–Jaworski-match support only | `THEOREM.md` §5.4–5.5 |
| Theorem J + Corollary (uniform restriction; exact `\tfrac12` same-cycle split, all finite `n,K`) | **PROVED**, elementary, adversarially verified (33/33 cells, 0 discrepancies) | Estágio 25 |
| `P(\text{same cycle}\mid K)\to1/(2(K{+}1))` for `K=0,1,2,3` | **PROVED**, by transfer (not direct continuum construction) | Estágios 28, 31, 35 |
| `P_{nn}(n,K)` closed forms, `K=1,2,3` | **PROVED**, exact finite-`n`, adversarially verified (independent brute force up to `n=10`, `K=2`, and `n=9`, `K=3`) | Estágios 27, 31, 35 |
| `E[(M_n^{(1)})^2]=\tfrac12+\tfrac1{2n^2}` | **PROVED**, exact all `n` | Estágio 27 (Corollary D1.2) |
| Governing-Source Reindexing, Cycle-Predecessor Uniqueness, at `K=3` | **PROVED**, adversarially verified (two independent verification layers, zero discrepancies) | Estágio 35 |
| The same two mechanisms, plus a general-`K` Lemma-5 analogue, plus `P_{nn}(n,K)` closed forms for `K=4,5,6` (Propositions NN4/NN5/NN6) | **PROVED but PENDING INTERNAL REVIEW** — computed and independently cross-checked by the front's own multiple routes (true brute force to `\sim1.65\times10^8` configurations at `K=4`; symbolic derivation; large-`n` numeric cross-checks beyond the fitting range) but **not yet dispatched to, or passed by, this archive's adversarial referee process**, hence **not yet an "Estágio"** | `theorem/conjecture2_direct_attempt/joint_two_point_attempt/joint_exploration_continuum_attempt/k2_joint_case_split_attempt/k3_joint_structural_attempt/general_k_joint_attempt/ATTEMPT.md` |
| Single closed-form-in-`K` formula for `P_{nn}(n,K)` (`K` symbolic, not case-by-case) | **OPEN** — precisely diagnosed (term-count growth: `2^{K-1}`/`3^{K-2}` terms; a concrete but unexecuted route via a rook-polynomial/EGF identity is named) | Same document, §8 |
| The full CDF of `M_n^{(K)}` for `K\ge2` (beyond the second moment) | **OPEN** | Estágios 27, 35 |
| The crossover regime `K` comparable to `n` (e.g. `K=\gamma n`) | **NOT ANALYZED ANYWHERE IN THIS ARCHIVE** | — |
| `\varphi(n,n)=Q(n)/n` (the `K=n`/`c=n` endpoint identity, Ramanujan's `Q`) | **PROVED**, exact all `n` (background context, outside this note's required-reading list, read directly by this note's author) | `theorem/uniform_in_c_attempt/ATTEMPT.md` §7.1, Proposição 7.1, integrated as `THEOREM.md` "Estágio 10" |

**On the "pending internal review" item specifically.** The general-`K`
document (§3.6/§5) is, in its own words, "PARTIAL CLOSURE, substantial":
its two structural mechanisms are shown to generalize to every `K` with
literally the same proof (no `K`-specific step); its Lemma-5 analogue
(closed-form single-point and cross-arc formulas, general `K`) is new and
general; its assembly algorithm is proved correct for any concrete `K`
and, run at `K=1,2,3`, **exactly reproduces** the already-adversarially-verified
closed forms of Estágios 27/31/35 — a strong self-consistency check. It
has not, as of this writing, been reviewed by this archive's dedicated
hostile-referee process, and this note does not treat it as an
established result; §3.5–3.6 above cite only what has already passed
that process (`K=1,2,3`), and flag the `K=4,5,6` extension and the
general-`K` mechanism proofs explicitly as pending.

---

## 5. Why might this interest a specialist in random mappings

Stated plainly, without overselling: **this looks like a modest-interest
case, not a major one**, and the honest reasons to flag it at all are
narrow and specific.

**What is *not* the source of interest.** Object A is not a new
asymptotic universality class. At both of its defining endpoints it
recovers exactly the classical objects: `K=0` is a bare permutation;
`K=n` is exactly Kolchin's uniform random mapping (§2), with the archive's
own exact identity `\varphi(n,n)=Q(n)/n` tying the `K=n` corner directly
to the classical `Q`-function asymptotics already used by Knuth and by
Flajolet–Odlyzko. The `K`-conditional limiting density itself (§3.1–3.2)
is not new — it is, at the level of functional form and mean, Hansen &
Jaworski's Theorem 7(ii) from a structurally different microscopic model
(in-degree-restricted uniform mappings, not permutation-plus-reroute).
And this archive's own priority search (`priority_search/`, wave 4,
`DISC-DEC-015` front A — quoted, not re-derived, here) already concluded
this directly: the individual pieces (permutation cycle statistics,
Poisson-Dirichlet limit, the `K`-conditional density, the `\sqrt n`
cyclic-point scaling) are all classical; the archive's own most
defensible novelty claim was about the **Poisson-mixture-in-`c` closed
form** `\varphi_\infty(c)=\int_0^1e^{-ct^2}dt`, a fact about a *different*
regime (the continuum limit `L(c)` under Poissonized, not exactly-`K`,
reroutes) than the finite-`n`, fixed-`K` results this note foregrounds.

**What might genuinely be worth a specialist's five minutes.**

1. **Exact finite-`n` formulas for fixed, general `K`, not just
   asymptotics.** Hansen–Jaworski's Theorem 7(ii) and the classical
   Kolchin/Flajolet–Odlyzko results are local-limit/asymptotic statements.
   `THEOREM.md`'s Proposition 4 (`\varphi_n^{(1)}=\tfrac23+\tfrac1{3n^2}`,
   exact for **every** `n\ge1`) and Estágio 31/35's `P_{nn}(n,K)` closed
   forms (exact rational functions of `n`, for `K=2,3`, with the
   `K=4,5,6` extensions pending review) are a different kind of object: a
   finite-`n` correction term, in closed form, for a specific, elementary
   member of the random-mappings family. Whether this specific family of
   exact finite-`n` corrections is itself already known (e.g. as a special
   case of some finite-`n` refinement of Hansen–Jaworski's own machinery)
   is **not established either way by this note** — it was not searched
   for beyond the archive's own wave-4 priority search, which targeted the
   `n\to\infty` results, not these finite-`n` ones.
2. **Theorem J (§3.3): an exact, finite-`n`, `n,K`-uniform bijective fact**
   — the restriction of the rerouted mapping to its own eventual cycle set
   is Haar-uniform, for every `n,K`. This is elementary once stated, but
   is a clean, self-contained lemma about the reroute-permutation model
   specifically (it uses the mixed permutation/independent-reroute
   structure, not a generic random-mapping argument) and was not located
   as a named prior result in the archive's own literature search.
3. **A different microscopic route to the same limiting `K`-conditional
   density.** That a permutation-plus-independent-Bernoulli-reroute
   construction and an in-degree-restricted uniform-mapping construction
   converge to the *same* conditional law is the kind of small
   universality fact that specialists in this area do sometimes find
   worth a remark, even when neither side's asymptotic content is new by
   itself — precisely because it is evidence the limiting object is a
   genuine attractor for "permutation-like backgrounds corrupted by a
   fixed number of independent defects," not an artifact of one
   particular microscopic recipe.
4. **Two small, clean, general-purpose lemmas** (Governing-Source
   Reindexing; Cycle-Predecessor Uniqueness, §3.6) about `K` marked
   sources embedded in a random functional digraph. Both are elementary
   once stated and plausibly folklore in the area (the pending-review
   document itself connects the underlying combinatorial identity —
   `\sum_kk!\,e_k(x_1,\ldots,x_m)=\int_0^\infty e^{-\lambda}\prod_j
   (1+x_j\lambda)\,d\lambda` — to classical rook-polynomial/permanent
   theory, not claiming it as new); they were simply not located by this
   archive's own search, and are stated here in a form a specialist could
   check against their own background in one pass.

**Net assessment.** The most defensible framing is: Object A is a natural,
easy-to-state variant that sits exactly on the line between two very
well-studied classical objects, reproduces both endpoints exactly (one
trivially, one by a genuine finite-`n` identity), reproduces a known
`n\to\infty` local-limit law from a different microscopic mechanism at
fixed `K`, and contributes a handful of exact finite-`n` closed forms plus
two small structural lemmas that a specialist has not, as far as this
archive's own (non-exhaustive, honestly caveated) search could tell, seen
stated this way before. That is plausibly worth a short remark or a
paragraph in a survey of the area — not, on the evidence assembled here, a
standalone result of major independent interest. Nothing in this
assessment should be read as a claim that the object is "new" in any
absolute sense; only that it was not found, in the searches this archive
has actually run.

---

## 6. On the archive's own literature search (context, not re-verified here)

This note relies for its "not found in the literature" claims on the
archive's own prior priority search
(`priority_search/PRIORITY_SEARCH.md`, `priority_search/SEARCH_LOG.md`,
wave 4, `DISC-DEC-015` front A — 22 documented searches, WebSearch and
WebFetch, including reported negatives and one explicitly inaccessible
source), which this note's author read directly but did not re-run or
independently extend. Its own summary, verdict by component: the
permutation-plus-independent-reroute *model itself* — not found (the
entire Jaworski/Hansen–Jaworski lineage, 1984 through 2014, is
parametrized by exchangeable in-degree sequences, never by a background
permutation corrupted by independent per-point rerouting); the
`\mathrm{PD}(1)`+Poisson-marks limit object — classical components,
novel combination not located as a named object; the `K`-conditional law
— **already known** (Hansen–Jaworski Theorem 7(ii), §3.2); the
Poisson-mixture-in-`c` closed form via `\mathrm{erf}` — not located,
flagged as the strongest novelty candidate (a claim about the `L(c)`
continuum-limit object, not about Object A's finite-`n`, fixed-`K` facts
that are the focus of this note); the `c^{-1/2}` tail exponent —
universal in the area (Kolchin; Flajolet–Odlyzko), the exact coefficient
and purely-exponential correction term specific to this ensemble. That
search explicitly flags one open honesty caveat still unresolved as of
this writing: **Kolchin's *Random Mappings* (1986) full text was not
accessible during that search**, so it remains — per the archive's own
words — "reported as inaccessible, not confirmed absent" as a possible
antecedent under different terminology. This note's own verification pass
(§7) confirms Kolchin's book's basic bibliographic details (publisher,
translation lineage) via public sources, but did **not** obtain or read
its full text either, and so carries forward the same caveat.

---

## 7. Citation verification note

Per this front's mandate, the two citations central to this note's
framing paragraph (§2) that were not already verbatim-verified elsewhere
in this archive were checked against public bibliographic sources before
use here (WebSearch, 2026-08-27):

- **Kolchin, V. F., *Random Mappings*.** Confirmed: published by
  Optimization Software, Inc. Publications Division, New York, 1986,
  in the *Translations Series in Mathematics and Engineering*
  (ISBN 0-387-96154-2 / 0-911575-16-2), as an English translation of
  *Slučajnye Otobraženija* (Nauka, Moscow, 1984). This matches, and adds
  the translation provenance to, the citation already used in this
  archive's own `tamesis-cycle-survival/paper/cycle-survival.bib`
  (`kolchin1986`). **Not independently verified: the book's full text**
  (as already flagged by the archive's own priority search, §6, and
  unresolved by this note).
- **Flajolet, P. & Odlyzko, A. M., "Random Mapping Statistics."**
  Confirmed: presented at EUROCRYPT '89 (Houthalen, Belgium, 1989);
  published in *Advances in Cryptology — EUROCRYPT '89*, ed. J.-J.
  Quisquater & J. Vandewalle, Lecture Notes in Computer Science vol. 434,
  Springer, Berlin/Heidelberg, pp. 329–354 (proceedings volume dated
  1990, standard for this LNCS series). This matches the citation already
  used, in the same "EUROCRYPT'89" short form, in this archive's own
  `theorem/uniform_in_c_attempt/ATTEMPT.md` §7.1.

No other citation in this note was independently re-verified beyond what
the archive's own already-verified `.bib` file and `THEOREM.md`/Estágio
text already record (Kingman 1975; Hansen & Jaworski 2014; Scheffé 1947;
Le Cam 1960; Arratia–Barbour–Tavaré 2003; Pitman 2002) — those are reused
verbatim from that existing, already-verified record.

---

## 8. Explicit scope discipline

No file other than this one was created or modified by this front.
`THEOREM.md`, `DECISION_LEDGER.yaml`, `TEST_QUEUE.yaml`,
`DISCOVERY_LAB_STATE.md`, `PROOF_DEPENDENCY_MAP.md`, `README.md`, and
`index.html` were read where relevant for context but **not touched**. No
`git` command was run. No new mathematical claim, derivation, proof, or
conjecture is made anywhere in this document — every mathematical
statement above is a restatement of an already-PROVED result (with its
Estágio/section cited) or is explicitly labeled CONJECTURE, PENDING
REVIEW, or OPEN, matching the source document's own label. **No claim of
progress on any Millennium Prize Problem, or any other famous unsolved
problem, is made anywhere in this document** — this is a positioning note
about a self-contained internal combinatorics object, full stop.
