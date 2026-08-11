/-
NS-5A (Wave-5, item WAVE5-NS-5A) — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`CalderonZygmundKernelDefinitions.lean`, `CalderonZygmundLocalPVExistence.lean`
(NS-1, Wave-1), `K_LipschitzDifference_HasLocalPV.lean` (NS-2a, Wave-2),
`PVDistributionOnCompactK.lean` (NS-2b, Wave-2),
`RadiusIndependencePVLipschitz.lean` (NS-3a, Wave-3) e
`PVFunctionalOnArbitraryCompactK.lean` (NS-4a, Wave-4), mesma pasta:
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra
o mesmo projeto Mathlib. Wave-5 é follow-on direto de Wave-4 (14 itens
fechados) e das três ondas anteriores a ela; item NS-5a do plano
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_5_2026_08_11.md`.

## O que esta frente tenta, e por que

`PVFunctionalOnArbitraryCompactK.lean` (NS-4a) prova
`pvKCLM_comp_monoCLM_eq_integral` para um compacto `K' : Compacts E`
ARBITRÁRIO (fixo) mais `pvKCLM_comp_monoCLM_radius_independent`, que
fixa ESSE MESMO `K'` e varia o raio-envelope `R` entre dois valores
`R1, R2 > 0` tais que `K' ⊆ closedBall 0 R1` e `K' ⊆ closedBall 0 R2`.
Em nenhum lugar de NS-4a dois compactos DECLARADOS DIFERENTES `K1 ≤ K2`
são comparados entre si — a "monotonicidade cruzada-compacta" nomeada
no plano da Onda 5.

Este arquivo fecha exatamente esse gap, pela rota "barata" de
composição já identificada no plano de ataque: para `K1 ≤ K2 : Compacts
E`, `f : 𝓓^{1}_{K1}(E, ℝ)`, e dois raios-envelope `R1, R2 > 0` com
`K1 ⊆ closedBall 0 R1` e `K2 ⊆ closedBall 0 R2` (logo, por
transitividade, `K1 ⊆ closedBall 0 R2` também), o valor de `pvKCLM`
aplicado à inclusão DIRETA `K1 → envelope R1` é igual ao valor de
`pvKCLM` aplicado à inclusão em DOIS PASSOS `K1 → K2 → envelope R2`.
Isto é, o valor do funcional p.v. não depende de rotear a inclusão
através de um compacto intermediário maior `K2`, nem da escolha do raio
de envelope em cada etapa.

A prova segue EXATAMENTE os três passos do teste falsificável do plano
de ataque (nada além disso é tentado):

1. Mostrar que a dupla composição `monoCLM ℝ (monoCLM ℝ f : K2) :
   envelope R2` e a composição direta `monoCLM ℝ f : K1 → envelope R2`
   produzem o MESMO VALOR de `pvKCLM e2 e3 R2 hR2`. Isso é feito
   aplicando `monoCLM_apply` (Mathlib) duas vezes (uma para cada estágio
   da dupla composição) para reduzir ambos os lados à MESMA fórmula
   integral via `pvKCLM_comp_monoCLM_eq_integral` (NS-4a) — nenhum
   "diamante de composição" custom de `monoCLM` é necessário: as duas
   composições concordam como FUNÇÕES subjacentes (`f`), então
   `pvKCLM_apply`/`pvKCLM_comp_monoCLM_eq_integral` (que só dependem dos
   valores da função, não de como o elemento de `ContDiffMapSupportedIn`
   foi construído) dão a mesma integral para ambos.
2. Invocar `pvKCLM_comp_monoCLM_radius_independent` (NS-4a, já
   provado) com `K' := K1`, relacionando o valor em `R1` e o valor em
   `R2`, ambos via a inclusão direta `K1 → envelope`.
3. Encadear (1) e (2) via `Eq.trans`.

## Restatação verbatim + import direto do artefato compilado de NS-4a

Diferentemente de NS-3a/NS-4a (que restatam TODO o conteúdo de suas
dependências verbatim, por não poderem `import` um arquivo irmão sem
`.olean` em `LEAN_PATH`), esta frente usa o mecanismo documentado no
protocolo de verificação da Onda 5 para o "known wrinkle": o artefato
`PVFunctionalOnArbitraryCompactK.olean` foi compilado diretamente para
`05_FORMAL/lean/.lake/build/lib/lean/PVFunctionalOnArbitraryCompactK.olean`
via
```
lake env lean -R <pasta-FORMAL-de-NS-4a> \
  <pasta-FORMAL-de-NS-4a>/PVFunctionalOnArbitraryCompactK.lean \
  -o .lake/build/lib/lean/PVFunctionalOnArbitraryCompactK.olean
```
(rodado a partir de `05_FORMAL/lean`, escrevendo SOMENTE no diretório
`.lake/` ignorado pelo git). Isso permite `import
PVFunctionalOnArbitraryCompactK` abaixo, evitando restatar as ~1150
linhas de maquinária de NS-1/NS-2a/NS-2b/NS-3a/NS-4a que este arquivo
não modifica. O CONTEÚDO de NS-4a permanece intocado (nenhum arquivo
fora deste é editado por esta sessão); só seu artefato de build,
gitignored, foi preenchido no cache compartilhado, exatamente como
documentado como aceitável no protocolo desta onda. O único conteúdo
NOVO desta frente é o teorema `pvKCLM_cross_compact_monotone` abaixo
(mais os dois `have` de igualdade de função subjacente que o alimentam)
— nenhuma outra definição/teorema é declarado neste arquivo.
-/

import PVFunctionalOnArbitraryCompactK

namespace TamesisNSPVEnvelopeCrossCompactMonotonicity

open TamesisNSPVFunctionalOnArbitraryK
open TopologicalSpace MeasureTheory

/-! ## NOVO NESTA FRENTE (NS-5a)

Único conteúdo novo desta sessão: `pvKCLM_cross_compact_monotone`, o
teste falsificável do plano de ataque, provado exatamente pela rota de
três passos descrita ali (composição barata + `pvKCLM_comp_monoCLM_radius_independent`
+ encadeamento). -/

/-- **Teorema-alvo (NS-5a).** Monotonicidade cruzada-compacta do
funcional p.v. envelope: para dois compactos DECLARADOS DIFERENTES
`K1 ≤ K2`, uma função-teste `f ∈ 𝓓^{1}_{K1}(E, ℝ)`, e dois
raios-envelope `R1, R2 > 0` com `K1 ⊆ closedBall 0 R1` e
`K2 ⊆ closedBall 0 R2`, o valor de `pvKCLM` aplicado à inclusão DIRETA
`K1 → envelope R1` é igual ao valor de `pvKCLM` aplicado à inclusão em
DOIS PASSOS `K1 → K2 → envelope R2`. Em particular, o valor do
funcional p.v. composto não depende de rotear a inclusão através de um
compacto intermediário `K2` estritamente maior que `K1`, nem da escolha
independente do raio de envelope em cada etapa da rota. -/
theorem pvKCLM_cross_compact_monotone
    (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (K1 K2 : Compacts (EuclideanSpace ℝ (Fin 3)))
    (R1 R2 : ℝ) (hR1 : 0 < R1) (hR2 : 0 < R2)
    (hK1K2 : K1 ≤ K2)
    (hK1R1 : K1 ≤ pvKCompact R1)
    (hK2R2 : K2 ≤ pvKCompact R2)
    (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K1) :
    pvKCLM e2 e3 R1 hR1
        (ContDiffMapSupportedIn.monoCLM ℝ f :
          ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R1))
      = pvKCLM e2 e3 R2 hR2
        (ContDiffMapSupportedIn.monoCLM ℝ
            (ContDiffMapSupportedIn.monoCLM ℝ f :
              ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
          ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2)) := by
  -- Transitividade: `K1 ⊆ K2 ⊆ envelope R2`, logo `K1 ⊆ envelope R2`.
  have hK1R2 : K1 ≤ pvKCompact R2 := hK1K2.trans hK2R2
  -- Passo (1): a inclusão em dois passos `K1 → K2 → envelope R2`, como
  -- FUNÇÃO subjacente, é literalmente `f` — via `monoCLM_apply`
  -- (Mathlib) aplicado duas vezes, uma por estágio.
  have hstep1 : ((ContDiffMapSupportedIn.monoCLM ℝ f :
      ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
      EuclideanSpace ℝ (Fin 3) → ℝ) = (f : EuclideanSpace ℝ (Fin 3) → ℝ) := by
    rw [ContDiffMapSupportedIn.monoCLM_apply, if_pos ⟨le_refl _, hK1K2⟩]
  have hstep2 : ((ContDiffMapSupportedIn.monoCLM ℝ
      (ContDiffMapSupportedIn.monoCLM ℝ f :
        ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
      ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2)) :
      EuclideanSpace ℝ (Fin 3) → ℝ) = (f : EuclideanSpace ℝ (Fin 3) → ℝ) := by
    rw [ContDiffMapSupportedIn.monoCLM_apply, if_pos ⟨le_refl _, hK2R2⟩, hstep1]
  -- Consequência: `pvKCLM` na dupla composição reproduz a MESMA fórmula
  -- integral que `pvKCLM_comp_monoCLM_eq_integral` (NS-4a) dá para a
  -- composição direta `K1 → envelope R2`.
  have hA : pvKCLM e2 e3 R2 hR2
      (ContDiffMapSupportedIn.monoCLM ℝ
          (ContDiffMapSupportedIn.monoCLM ℝ f :
            ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
        ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2))
      = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
          {(0 : EuclideanSpace ℝ (Fin 3))}),
          K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0) := by
    have hraw := pvKCLM_comp_monoCLM_eq_integral e2 e3 K2 R2 hR2 hK2R2
      (ContDiffMapSupportedIn.monoCLM ℝ f :
        ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2)
    rwa [hstep1] at hraw
  have hB : pvKCLM e2 e3 R2 hR2
      (ContDiffMapSupportedIn.monoCLM ℝ f :
        ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2))
      = ∫ y in (Metric.closedBall (0 : EuclideanSpace ℝ (Fin 3)) R2 \
          {(0 : EuclideanSpace ℝ (Fin 3))}),
          K e2 e3 y * ((f : EuclideanSpace ℝ (Fin 3) → ℝ) y - f 0) :=
    pvKCLM_comp_monoCLM_eq_integral e2 e3 K1 R2 hR2 hK1R2 f
  have hDirect_eq_double :
      pvKCLM e2 e3 R2 hR2
          (ContDiffMapSupportedIn.monoCLM ℝ f :
            ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2))
        = pvKCLM e2 e3 R2 hR2
          (ContDiffMapSupportedIn.monoCLM ℝ
              (ContDiffMapSupportedIn.monoCLM ℝ f :
                ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
            ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) (pvKCompact R2)) :=
    hB.trans hA.symm
  -- Passo (2): independência de raio já provada em NS-4a, aplicada com
  -- `K' := K1` (não `K2`) — relaciona a inclusão direta `K1 → envelope`
  -- entre os dois raios `R1` e `R2`.
  have hRadius := pvKCLM_comp_monoCLM_radius_independent e2 e3 K1 R1 R2 hR1 hR2 hK1R1 hK1R2 f
  -- Passo (3): encadear.
  exact hRadius.trans hDirect_eq_double

#print axioms pvKCLM_cross_compact_monotone

end TamesisNSPVEnvelopeCrossCompactMonotonicity

/-! ## O que NÃO é afirmado

```text
NÃO constrói um membro de `𝓓^{1}(E, ℝ) →L[ℝ] ℝ` (dual topológico do
  espaço COMPLETO de funções-teste) -- mesmo gap (iii) já escopado para
  fora em NS-4a, inteiramente fora do escopo desta frente também
NÃO prova nenhuma limitação L^p de operador integral singular
NÃO prova nenhum teorema de Calderón-Zygmund (decomposição, tipo-fraco,
  interpolação de Marcinkiewicz)
NÃO trata uma função-teste genérica de Schwartz/C^∞_c de ordem
  arbitrária -- só `𝓓^{1}_{K1}` (ordem exatamente `1`, `e2`, `e3`
  continuam fixos, "coeficientes congelados")
NÃO prova nada sobre a integral p.v. real das equações (2.1)/(2.2) de
  Constantin-Fefferman aplicada a um campo de vorticidade genuíno
NÃO prova NS-GAP-001/002/004/005 nem qualquer regularidade condicional
  real -- `GAP_REGISTER.yaml` de `02_NAVIER_STOKES` não é tocado
NÃO afirma que Navier-Stokes ficou alcançável, aproximável, ou resolvido
NÃO afirma novidade matemática -- é uma consequência elementar de
  composição de `ContinuousLinearMap`s já fechados (`monoCLM` do
  Mathlib, `pvKCLM_comp_monoCLM_eq_integral` e
  `pvKCLM_comp_monoCLM_radius_independent` de NS-4a): a "rota barata"
  de composição do teste falsificável do plano de ataque elaborou
  LIMPA, sem nenhum "diamante de composição" -- ambos os lados da
  composição dupla, como funções subjacentes, colapsam a `f`
  diretamente via duas aplicações de `monoCLM_apply` do Mathlib, e daí
  em diante a prova é pura reescrita/encadeamento de lemas já fechados
NÃO modifica `PVFunctionalOnArbitraryCompactK.lean` (NS-4a) nem
  qualquer outro arquivo de onda anterior -- só seu artefato de build
  `.olean` (gitignored) foi preenchido no cache compartilhado
  `05_FORMAL/lean/.lake/build/lib/lean/`, para permitir `import` direto
  em vez de restatação verbatim de ~1150 linhas
```
-/
