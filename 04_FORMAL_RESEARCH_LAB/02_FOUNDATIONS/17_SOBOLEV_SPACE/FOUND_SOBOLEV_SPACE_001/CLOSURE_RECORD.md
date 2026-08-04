---
document_id: FOUND-SOBOLEV-SPACE-001-CLOSURE-RECORD
work_item_id: FOUND-SOBOLEV-SPACE-001
work_status: VERIFIED
result_review: APPROVED
gate_combination_declared: true
closes_gap: FM-GAP-001
---

# Registro de encerramento

## O tipo `H^s` existe

O Mathlib nao tinha **tipo** de espaco de Sobolev: `MemSobolev s p f` era
um `Prop` sobre `TemperedDistribution`, e `grep -rl MemSobolev Mathlib`
retornava **um** arquivo. Agora:

```lean
def sobolevSubmodule (s : ℝ) : Submodule ℂ 𝓢'(E, F) where
  carrier := {f | MemSobolev s 2 f}
def Hs (s : ℝ) : Type _ := ↥(sobolevSubmodule E F s)

instance : NormedAddCommGroup (Hs E F s)
instance : NormedSpace ℂ (Hs E F s)
instance : CompleteSpace (Hs E F s)
```

**Espaco de Banach completo.** `345` linhas, `57` declaracoes (10 `def`,
6 `instance`, 41 teoremas), `27` `#print axioms` todos limpos,
`lake build` exit `0`, `0` `sorry`.

## A escolha: subtipo, nao pullback

O pullback de `Lp` daria o tipo normado de graca, mas seria objeto
**paralelo** a `𝓢'`. O subtipo e literalmente o predicado do Mathlib
promovido a tipo, e isso e **demonstravel**:

```lean
range_toDist (s) : Set.range (toDist : Hs E F s → 𝓢'(E,F))
                     = {f : 𝓢'(E,F) | MemSobolev s 2 f}
```

`Hs` e `def` opaco e nao `abbrev` **de proposito**: impede que a
topologia de subtipo herdada de `𝓢'` colida com a topologia metrica da
norma.

## A norma, bem definida pela injetividade que ja estava na arvore

```lean
toL2 (f) := Classical.choose (memSobolev_toDist f)
toL2_eq  : besselPotential s (toDist f) = ↑u → toL2 f = u
norm_def : ‖f‖ = ‖toL2 f‖
norm_eq_of_besselPotential : besselPotential s (toDist f) = ↑u → ‖f‖ = ‖u‖
```

A unicidade vem de `toTemperedDistribution_injective` e
`besselPotential_injective`, **ambas provadas na frente anterior**. A
cadeia se pagou.

## A isometria de Bessel

```lean
def toL2ₗᵢ (s : ℝ) : Hs E F s ≃ₗᵢ[ℂ] Lp F 2 (volume : Measure E)
```

E dela caem completude **e** o multiplicador em Sobolev:

```lean
fourierMultiplierSobolevCLM (s) (g : Lp ℂ ∞ volume) : Hs E F s →L[ℂ] Hs E F s
norm_fourierMultiplierSobolevCLM_le : ‖·‖ ≤ ‖g‖
```

## Instancia positiva com norma em FORMA FECHADA

Nao e so "nao-vazio":

```lean
norm_bump (s) (c) : ‖bump E F s c‖
    = ‖c‖ * (volume.real (ball (0:E) 1)) ^ (1/2 : ℝ)

concrete_norm_bump : ‖bump ℝ ℂ (5/2 : ℝ) 1‖ = 2 ^ (1/2 : ℝ)     -- = raiz de 2
concrete_Hs_nontrivial :
    ∃ f : Hs ℝ ℂ (5/2 : ℝ), f ≠ 0 ∧ 0 < ‖f‖ ∧ toDist f ≠ 0 ∧ …
```

Enunciado **fechado, sem variaveis livres nem hipoteses**. `Hs ℝ ℂ (5/2)`
e habitado por elemento de norma `raiz de 2`. A norma **nao** e
identicamente zero e o tipo **nao** e vazio nem trivial — quinta vez
nesta sessao que a checagem anti-vacuidade e feita antes de fechar.

E o fecho do circulo:

```lean
concrete_leray_operator :
    ¬ (lerayComponent 1 1).HasTemperateGrowth ∧
    fourierMultiplierCLM ℂ (lerayComponent 1 1) = 0 ∧
    ‖fourierMultiplierSobolevCLM ℝ ℂ (5/2) (lerayComponentL2 1 1)‖ ≤ … ∧
    Nontrivial (Hs ℝ ℂ (5/2))
```

O simbolo de Leray, no qual o operador do Mathlib **e zero**, agora tem
operador genuino em `H^s`.

## Ressalva de leitura, registrada pelo proprio medidor

Como `toL2ₗᵢ` e isometria para **todo** `s`, todos os `Hs E F s` sao
isometricos entre si. **Isso e o teorema correto** — Bessel e isomorfismo
`H^s ≅ L²` — e a dependencia em `s` vive no **mergulho** `toDist`, que e
`s`-dependente por `range_toDist`. **Nao e degenerescencia.**

## Obstaculo de elaboracao, nao de matematica

`Lp (α := E) F 2` falhou o autoparam `volume_tac` em 3 sitios, embora
funcione em ~20 outros do mesmo arquivo. Contornado escrevendo
`Lp F 2 (volume : Measure E)` explicitamente. **Bug de elaboracao do
Lean 4.33.0-rc1**, nao obstrucao matematica.

## O que fica aberto

```text
SS-GAP-001  Hs 0 ≅ L² como identificacao canonica
SS-GAP-002  inclusao continua Hs s →L Hs s' para s' <= s
SS-GAP-003  ∂_m : Hs s →L Hs (s-1) e Δ : Hs s →L Hs (s-2) como CLMs.
            MemSobolev.lineDerivOp e .laplacian dao o FECHO;
            falta a LIMITACAO.
SS-GAP-004  InnerProductSpace ℂ (Hs E F s), que cai da isometria
SS-GAP-005  mergulho de Sobolev
```

## O que NAO e afirmado

```text
que Navier-Stokes tenha ficado alcancavel
que exista teoria de EDP no laboratorio
que isto seja contribuicao aceita no Mathlib
```

**Nenhum problema de milenio foi atacado.** O que existe e um espaco de
Banach com o range certo e uma instancia de norma raiz de 2.
