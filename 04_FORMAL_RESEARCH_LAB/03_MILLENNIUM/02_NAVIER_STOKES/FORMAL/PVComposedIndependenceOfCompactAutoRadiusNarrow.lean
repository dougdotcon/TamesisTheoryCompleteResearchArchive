/-
NS-7A (Wave-7, item WAVE7-NS-7A) — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`CalderonZygmundKernelDefinitions.lean`, `CalderonZygmundLocalPVExistence.lean`
(NS-1, Wave-1), `K_LipschitzDifference_HasLocalPV.lean` (NS-2a, Wave-2),
`PVDistributionOnCompactK.lean` (NS-2b, Wave-2),
`RadiusIndependencePVLipschitz.lean` (NS-3a, Wave-3),
`PVFunctionalOnArbitraryCompactK.lean` (NS-4a, Wave-4),
`PVEnvelopeCrossCompactMonotonicity.lean` (NS-5a, Wave-5) e
`PVCrossCompactMonotonicityAutoRadius.lean` (NS-6a, Wave-6), mesma pasta:
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra
o mesmo projeto Mathlib. Wave-7 é follow-on direto de Wave-6 (13 itens
fechados, a segunda onda inteiramente limpa consecutiva) e das cinco
ondas anteriores a ela; item NS-7a do plano
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_7_2026_08_11.md`.

## O que esta frente tenta, e por que

`PVFunctionalOnArbitraryCompactK.lean` (NS-4a, Parte 10) prova
`pvKCLM_comp_monoCLM_radius_independent`: para UM ÚNICO compacto FIXO
`K' : Compacts E` e uma função-teste `f ∈ 𝓓^{1}_{K'}(E, ℝ)`, o valor do
funcional composto `pvKCLM e2 e3 R hR (monoCLM ℝ f)` não depende de qual
raio-envelope `R` (com `K' ⊆ closedBall 0 R`) é escolhido para calculá-lo
— duas hipóteses `hK'1 : K' ≤ pvKCompact R1`, `hK'2 : K' ≤ pvKCompact R2`
FORNECIDAS pelo chamador. `PVCrossCompactMonotonicityAutoRadius.lean`
(NS-6a) mostra, separadamente, que cada compacto individual admite um
raio-envelope AUTO-DERIVADO `autoEnvelopeRadius K` (via compacidade,
`Classical.choose`), eliminando a necessidade de o raio ser hipótese
livre — mas aplicado a `pvKCLM_cross_compact_monotone` (NS-5a), que
exige `K1 ≤ K2` (uma relação de ORDEM entre os dois compactos).

Esta frente (NS-7a) fecha o teste falsificável (estreitado, "narrow")
do plano de ataque da Onda 7: uma versão de independência de
compacto/raio do funcional COMPOSTO (`pvKCLM ∘ monoCLM`) que usa os
raios AUTO-DERIVADOS de NS-6a (nenhum raio como hipótese livre), para
DOIS COMPACTOS `K1 K2 : Compacts E` **SEM NENHUMA RELAÇÃO DE ORDEM ENTRE
ELES** (ao contrário de NS-5a/NS-6a, que exigem `K1 ≤ K2`) — daí
"estreitado": em vez de uma relação de ordem entre os compactos, a
hipótese de acoplamento é `hfun`, que as DUAS funções-teste `f1 ∈
𝓓^{1}_{K1}(E,ℝ)` e `f2 ∈ 𝓓^{1}_{K2}(E,ℝ)` têm a MESMA função subjacente
(`(f1 : E → ℝ) = (f2 : E → ℝ)`, isto é, são o MESMO elemento de
`𝓓^{1}(E,ℝ)` visto sob dois empacotamentos de suporte-compacto
possivelmente diferentes). Sob essa hipótese, o teorema-alvo mostra:

```
pvKCLM e2 e3 (autoEnvelopeRadius K1) _ (monoCLM ℝ f1)
  = pvKCLM e2 e3 (autoEnvelopeRadius K2) _ (monoCLM ℝ f2)
```

isto é, o valor do composto não depende nem do compacto-empacotamento
(`K1` vs `K2`) nem do raio-envelope auto-derivado correspondente,
CONTANTO que a função subjacente seja a mesma.

## Protocolo de duas fases (exatamente o teste falsificável do plano de
ataque, nada além disso é tentado)

**Fase (a).** `rw [pvKCLM_comp_monoCLM_eq_integral e2 e3 K1 ... f1,
pvKCLM_comp_monoCLM_eq_integral e2 e3 K2 ... f2, hfun]` (as duas
primeiras reescritas são a Parte 9 de NS-4a, restatada por `import`;
`hfun` reescreve a função subjacente de `f1` para a de `f2` nos dois
lugares em que ela aparece no integrando esquerdo, `(f1:E→ℝ) y` e `f1
0`). Como o plano previu, isso NÃO fecha em 2 linhas: o objetivo
residual é uma igualdade de duas integrais p.v. da MESMA função (`f2`)
sobre dois ANÉIS de raios DIFERENTES, `autoEnvelopeRadius K1` vs.
`autoEnvelopeRadius K2`.

**Fase (b).** Fecha-se o residual adaptando o método `wlog`/`hsupp` da
Parte 10 de NS-4a: `rcases lt_trichotomy (autoEnvelopeRadius K1)
(autoEnvelopeRadius K2)` de três casos.
- Se `autoEnvelopeRadius K1 < autoEnvelopeRadius K2`: o raio MÍNIMO é o
  de `K1`; usa-se a contenção de `K1` (`autoEnvelopeRadius_subset K1`,
  NS-6a) — para `‖y‖ > autoEnvelopeRadius K1`, `y ∉ K1`, logo
  `f1.zero_on_compl` dá `f1 y = 0`; `hfun` converte isso em `f2 y = 0`.
  Aplica-se `pv_value_radius_independent` (NS-3a) diretamente.
- Se os dois raios são iguais: `rw` fecha por `rfl`.
- Se `autoEnvelopeRadius K2 < autoEnvelopeRadius K1`: o raio MÍNIMO é o
  de `K2`; usa-se a contenção de `K2` (`autoEnvelopeRadius_subset K2`)
  e `f2.zero_on_compl` DIRETAMENTE (sem precisar de `hfun` neste ramo,
  pois o integrando já está em termos de `f2`); aplica-se
  `pv_value_radius_independent` com os dois raios trocados e `.symm`.

Isso é exatamente o protocolo pedido: "escolhendo a contenção de K1 ou
K2 conforme qual `autoEnvelopeRadius` é o mínimo".

## Restatação verbatim + import direto dos artefatos compilados de
NS-4a/NS-5a/NS-6a

Como em NS-6a, este arquivo usa o mecanismo documentado no protocolo de
verificação da Onda 5/6/7 para o "known wrinkle": os artefatos
`PVFunctionalOnArbitraryCompactK.olean` (NS-4a),
`PVEnvelopeCrossCompactMonotonicity.olean` (NS-5a) e
`PVCrossCompactMonotonicityAutoRadius.olean` (NS-6a) são compilados
diretamente para `05_FORMAL/lean/.lake/build/lib/lean/` via

```
lake env lean -R <pasta-FORMAL> <pasta-FORMAL>/<Arquivo>.lean \
  -o .lake/build/lib/lean/<Arquivo>.olean
```

(rodado a partir de `05_FORMAL/lean`, escrevendo SOMENTE no diretório
`.lake/` ignorado pelo git). Isso permite `import
PVCrossCompactMonotonicityAutoRadius` abaixo (que por sua vez importa
`PVEnvelopeCrossCompactMonotonicity` e `PVFunctionalOnArbitraryCompactK`
transitivamente), evitando restatar a maquinária de NS-1..NS-6a que
este arquivo não modifica. O CONTEÚDO de NS-4a/NS-5a/NS-6a permanece
intocado (nenhum arquivo fora deste é editado por esta sessão); só os
artefatos de build, gitignored, foram (re)preenchidos no cache
compartilhado se necessário. O único conteúdo NOVO desta frente é o
teorema-alvo `pvKCLM_comp_monoCLM_auto_radius_independent_of_eq_fun` —
nenhuma outra definição/teorema é declarado neste arquivo.
-/

import PVCrossCompactMonotonicityAutoRadius

namespace TamesisNSPVComposedIndependenceOfCompactAutoRadiusNarrow

open TamesisNSPVFunctionalOnArbitraryK
open TamesisNSPVCrossCompactMonotonicityAutoRadius
open TopologicalSpace MeasureTheory
open scoped Distributions

/-! ## NOVO NESTA FRENTE (NS-7a)

Único conteúdo novo desta sessão: o teste falsificável do plano de
ataque da Onda 7, `pvKCLM_comp_monoCLM_auto_radius_independent_of_eq_fun`,
provado pelo protocolo de duas fases descrito acima. -/

/-- **Teorema-alvo (NS-7a).** Independência de compacto/raio (auto-
derivado) do funcional p.v. composto, versão ESTREITADA: para dois
compactos `K1 K2 : Compacts E` SEM relação de ordem assumida entre eles,
e duas funções-teste `f1 ∈ 𝓓^{1}_{K1}(E,ℝ)`, `f2 ∈ 𝓓^{1}_{K2}(E,ℝ)` com a
MESMA função subjacente (`hfun`), o valor de `pvKCLM ∘ monoCLM` no raio
auto-derivado de `K1` aplicado a `f1` é igual ao valor no raio
auto-derivado de `K2` aplicado a `f2`. Compare com
`pvKCLM_comp_monoCLM_radius_independent` (NS-4a, Parte 10, um único
compacto/duas hipóteses de raio livres) e com
`pvKCLM_cross_compact_monotone_auto_radius` (NS-6a, dois compactos COM
`K1 ≤ K2`, raios auto-derivados, sem hipótese `hfun`). -/
theorem pvKCLM_comp_monoCLM_auto_radius_independent_of_eq_fun
    (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (K1 K2 : Compacts (EuclideanSpace ℝ (Fin 3)))
    (f1 : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K1)
    (f2 : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2)
    (hfun : (f1 : EuclideanSpace ℝ (Fin 3) → ℝ) = (f2 : EuclideanSpace ℝ (Fin 3) → ℝ)) :
    pvKCLM e2 e3 (autoEnvelopeRadius K1) (autoEnvelopeRadius_pos K1)
        (ContDiffMapSupportedIn.monoCLM ℝ f1)
      = pvKCLM e2 e3 (autoEnvelopeRadius K2) (autoEnvelopeRadius_pos K2)
        (ContDiffMapSupportedIn.monoCLM ℝ f2) := by
  -- Fase (a): duas reescritas via NS-4a Parte 9 + `hfun`; objetivo
  -- residual = igualdade de integrais de `f2` sobre dois anéis de raios
  -- diferentes (NÃO um fechamento de 2 linhas, como o plano previu).
  rw [pvKCLM_comp_monoCLM_eq_integral e2 e3 K1 (autoEnvelopeRadius K1)
        (autoEnvelopeRadius_pos K1) (autoEnvelopeRadius_subset K1) f1,
      pvKCLM_comp_monoCLM_eq_integral e2 e3 K2 (autoEnvelopeRadius K2)
        (autoEnvelopeRadius_pos K2) (autoEnvelopeRadius_subset K2) f2,
      hfun]
  -- Fase (b): fecha o residual via `pv_value_radius_independent` (NS-3a),
  -- com `wlog`/`hsupp` sobre qual `autoEnvelopeRadius` é o mínimo,
  -- exatamente como a Parte 10 de NS-4a.
  set L2 : ℝ := N[ℝ]_{K2, (1 : ℕ∞), 1} f2 with hL2def
  have hLip2 : LipschitzWith L2.toNNReal (f2 : EuclideanSpace ℝ (Fin 3) → ℝ) :=
    lipschitzWith_seminorm_of_contDiffMapSupportedIn f2
  rcases lt_trichotomy (autoEnvelopeRadius K1) (autoEnvelopeRadius K2) with hlt | heq | hlt
  · -- raio mínimo é o de `K1`: usa a contenção de `K1` via `f1`, `hfun`.
    have hsupp : ∀ y : EuclideanSpace ℝ (Fin 3),
        autoEnvelopeRadius K1 < ‖y‖ → (f2 : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := by
      intro y hy
      have hy1 : y ∉ (K1 : Set (EuclideanSpace ℝ (Fin 3))) := by
        intro hmem
        have hy' : y ∈ (pvKCompact (autoEnvelopeRadius K1) :
            Set (EuclideanSpace ℝ (Fin 3))) :=
          SetLike.coe_subset_coe.mpr (autoEnvelopeRadius_subset K1) hmem
        have hle : ‖y‖ ≤ autoEnvelopeRadius K1 := by
          simpa [pvKCompact, Metric.mem_closedBall, dist_zero_right] using hy'
        exact absurd hle (not_le.mpr hy)
      have hf1y : (f1 : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := f1.zero_on_compl hy1
      rw [← hfun]; exact hf1y
    exact pv_value_radius_independent e2 e3 (f2 : EuclideanSpace ℝ (Fin 3) → ℝ) L2 hLip2
      0 (autoEnvelopeRadius K1) (autoEnvelopeRadius K2) (autoEnvelopeRadius_pos K1) hlt hsupp
  · -- raios iguais: fecha por `rfl` após `rw`.
    rw [heq]
  · -- raio mínimo é o de `K2`: usa a contenção de `K2` via `f2` direto.
    have hsupp : ∀ y : EuclideanSpace ℝ (Fin 3),
        autoEnvelopeRadius K2 < ‖y‖ → (f2 : EuclideanSpace ℝ (Fin 3) → ℝ) y = 0 := by
      intro y hy
      have hy2 : y ∉ (K2 : Set (EuclideanSpace ℝ (Fin 3))) := by
        intro hmem
        have hy' : y ∈ (pvKCompact (autoEnvelopeRadius K2) :
            Set (EuclideanSpace ℝ (Fin 3))) :=
          SetLike.coe_subset_coe.mpr (autoEnvelopeRadius_subset K2) hmem
        have hle : ‖y‖ ≤ autoEnvelopeRadius K2 := by
          simpa [pvKCompact, Metric.mem_closedBall, dist_zero_right] using hy'
        exact absurd hle (not_le.mpr hy)
      exact f2.zero_on_compl hy2
    exact (pv_value_radius_independent e2 e3 (f2 : EuclideanSpace ℝ (Fin 3) → ℝ) L2 hLip2
      0 (autoEnvelopeRadius K2) (autoEnvelopeRadius K1) (autoEnvelopeRadius_pos K2)
      hlt hsupp).symm

#print axioms pvKCLM_comp_monoCLM_auto_radius_independent_of_eq_fun

end TamesisNSPVComposedIndependenceOfCompactAutoRadiusNarrow

/-! ## O que NÃO é afirmado

```text
NÃO constrói um membro de `𝓓^{1}(E, ℝ) →L[ℝ] ℝ` (dual topológico do
  espaço COMPLETO de funções-teste) -- mesmo gap (iii) já escopado para
  fora em NS-4a/NS-5a/NS-6a, inteiramente fora do escopo desta frente
  também
NÃO prova nenhuma limitação L^p de operador integral singular
NÃO prova nenhum teorema de Calderón-Zygmund (decomposição, tipo-fraco,
  interpolação de Marcinkiewicz)
NÃO trata uma função-teste genérica de Schwartz/C^∞_c de ordem
  arbitrária -- só `𝓓^{1}_{K}` (ordem exatamente `1`, `e2`, `e3`
  continuam fixos, "coeficientes congelados")
NÃO prova nada sobre a integral p.v. real das equações (2.1)/(2.2) de
  Constantin-Fefferman aplicada a um campo de vorticidade genuíno
NÃO prova NS-GAP-001/002/004/005 nem qualquer regularidade condicional
  real -- `GAP_REGISTER.yaml` de `02_NAVIER_STOKES` não é tocado
NÃO afirma que Navier-Stokes ficou alcançável, aproximável, ou resolvido
NÃO afirma novidade matemática -- é uma consequência elementar de (a)
  `pvKCLM_comp_monoCLM_eq_integral` (NS-4a, Parte 9), (b)
  `autoEnvelopeRadius`/`autoEnvelopeRadius_pos`/`autoEnvelopeRadius_subset`
  (NS-6a), e (c) `pv_value_radius_independent` (NS-3a) aplicado à função
  subjacente comum via `hfun` -- nenhum "diamante de composição" novo,
  nenhuma análise nova: o CONTEÚDO matemático é o mesmo case-split
  `min`/`max` já fechado em NS-4a Parte 10, só reempacotado para DOIS
  compactos SEM relação de ordem, acoplados pela hipótese `hfun` (função
  subjacente comum) em vez de uma hipótese `K1 ≤ K2`
NÃO afirma que a hipótese `hfun` é "automática" ou dispensável -- SEM
  ela, o resultado é falso em geral (dois compactos `K1 K2` disjuntos,
  com `f1`/`f2` funções-teste NÃO relacionadas, não têm por que produzir
  o mesmo valor de integral p.v.); `hfun` é uma hipótese GENUÍNA do
  teorema, não uma consequência de `K1`/`K2`
NÃO afirma que `autoEnvelopeRadius K` é o raio ÓTIMO/mínimo para `K`
  (mesma ressalva de NS-6a: `Bornology.IsBounded.subset_closedBall_lt`
  só garante EXISTÊNCIA de algum raio, via `Classical.choose`,
  `noncomputable`, sem fórmula fechada)
NÃO modifica `PVFunctionalOnArbitraryCompactK.lean` (NS-4a),
  `PVEnvelopeCrossCompactMonotonicity.lean` (NS-5a), nem
  `PVCrossCompactMonotonicityAutoRadius.lean` (NS-6a), nem qualquer
  outro arquivo de onda anterior -- só artefatos de build `.olean`
  (gitignored) foram (re)preenchidos no cache compartilhado
  `05_FORMAL/lean/.lake/build/lib/lean/`, para permitir `import` direto
  em vez de restatação verbatim de mais de 1300 linhas
```
-/
