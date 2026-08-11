/-
NS-6A (Wave-6, item WAVE6-NS-6A) — rascunho isolado, NÃO integrado a
`TamesisLab.lean`. Segue exatamente a convenção de
`CalderonZygmundKernelDefinitions.lean`, `CalderonZygmundLocalPVExistence.lean`
(NS-1, Wave-1), `K_LipschitzDifference_HasLocalPV.lean` (NS-2a, Wave-2),
`PVDistributionOnCompactK.lean` (NS-2b, Wave-2),
`RadiusIndependencePVLipschitz.lean` (NS-3a, Wave-3),
`PVFunctionalOnArbitraryCompactK.lean` (NS-4a, Wave-4) e
`PVEnvelopeCrossCompactMonotonicity.lean` (NS-5a, Wave-5), mesma pasta:
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra
o mesmo projeto Mathlib. Wave-6 é follow-on direto de Wave-5 (14 itens
fechados, a primeira onda inteiramente limpa deste ciclo) e das quatro
ondas anteriores a ela; item NS-6a do plano
`01_PORTFOLIO/PLANO_DE_ATAQUE_ONDA_6_2026_08_11.md`.

## O que esta frente tenta, e por que

`PVEnvelopeCrossCompactMonotonicity.lean` (NS-5a) prova
`pvKCLM_cross_compact_monotone`: para dois compactos DECLARADOS
DIFERENTES `K1 ≤ K2 : Compacts E`, uma função-teste
`f ∈ 𝓓^{1}_{K1}(E, ℝ)`, e dois raios-envelope `R1, R2 > 0` FORNECIDOS
EXPLICITAMENTE PELO CHAMADOR (junto com as hipóteses `K1 ⊆ closedBall 0
R1` e `K2 ⊆ closedBall 0 R2`), o valor de `pvKCLM` aplicado à inclusão
direta `K1 → envelope R1` é igual ao valor aplicado à inclusão em dois
passos `K1 → K2 → envelope R2`. Os raios `R1, R2` e as duas hipóteses de
inclusão-em-bola são, em NS-5a, hipóteses LIVRES do teorema — o chamador
escolhe os raios E prova que eles envelopam os compactos certos.

Esta frente (NS-6a) fecha exatamente o teste falsificável do plano de
ataque da Onda 6: mostrar que essas hipóteses de raio/envelope não
precisam ser dados de entrada nenhum — todo compacto `K : Compacts E` é,
por definição, um conjunto COMPACTO, logo (Mathlib,
`IsCompact.isBounded`) um conjunto LIMITADO, logo (Mathlib,
`Bornology.IsBounded.subset_closedBall_lt`) admite, ele mesmo, um raio
`r > 0` com `K ⊆ closedBall 0 r` — não é preciso que ninguém o forneça
"de fora". Usando `Classical.choose`/`Classical.choose_spec` sobre essa
existência, cada compacto `K` produz seu PRÓPRIO raio-envelope
`autoEnvelopeRadius K`, DERIVADO inteiramente de `K` (via sua
compacidade), nunca escolhido livremente pelo chamador. Instanciando
`pvKCLM_cross_compact_monotone` (NS-5a) com `R1 := autoEnvelopeRadius
K1` e `R2 := autoEnvelopeRadius K2` produz exatamente o teorema-alvo
desta frente, cujo ENUNCIADO final não menciona nenhum raio, nenhuma
hipótese de positividade de raio, e nenhuma hipótese de
inclusão-em-bola como argumento livre — só `e2 e3`, `K1 K2`, `hK1K2 :
K1 ≤ K2` e `f`. Os raios continuam existindo (o teorema `pvKCLM` exige
um raio-envelope para ser sequer aplicável), mas agora são
INTERNOS/DERIVADOS, não hipóteses do enunciado.

A prova segue EXATAMENTE a rota do teste falsificável do plano de
ataque (nada além disso é tentado):

1. Para `K : Compacts E`, `K.isCompact : IsCompact (K : Set E)`
   (Mathlib, `TopologicalSpace.Compacts.isCompact`, restatado/reusado
   diretamente, sem redeclarar); `IsCompact.isBounded` (Mathlib) dá
   `Bornology.IsBounded (K : Set E)`.
2. `Bornology.IsBounded.subset_closedBall_lt` (Mathlib,
   `Mathlib.Topology.MetricSpace.Bounded`) aplicado com limiar `a := 0`
   e centro `c := 0` dá `∃ r, 0 < r ∧ (K : Set E) ⊆ closedBall 0 r`.
   `Classical.choose`/`.choose_spec` extraem um raio concreto
   `autoEnvelopeRadius K` e as duas metades da conjunção
   (`autoEnvelopeRadius_pos`, positividade; e a inclusão em bola, usada
   no passo 3).
3. A inclusão em bola bruta (`Set ⊆ Set`) é convertida para a ordem de
   `Compacts E` (`K ≤ pvKCompact (autoEnvelopeRadius K)`, NS-4a) via
   `SetLike.coe_subset_coe` (Mathlib, `Mathlib.Data.SetLike.Basic`),
   explorando que `(pvKCompact R : Set E)` é DEFINICIONALMENTE
   `Metric.closedBall 0 R` (NS-4a, `pvKCompact` é literalmente
   `⟨closedBall 0 R, _⟩`).
4. `pvKCLM_cross_compact_monotone` (NS-5a, já fechado) é instanciado
   diretamente com `R1 := autoEnvelopeRadius K1`, `R2 :=
   autoEnvelopeRadius K2`, e as hipóteses de positividade/inclusão-em-
   bola dos passos 2-3. Nenhuma tática nova de análise é necessária —
   é literalmente aplicação de função a argumentos derivados.

## Restatação verbatim + import direto dos artefatos compilados de NS-4a/NS-5a

Como em NS-5a, este arquivo usa o mecanismo documentado no protocolo de
verificação da Onda 5/6 para o "known wrinkle": os artefatos
`PVFunctionalOnArbitraryCompactK.olean` (NS-4a) e
`PVEnvelopeCrossCompactMonotonicity.olean` (NS-5a) foram compilados
diretamente para
`05_FORMAL/lean/.lake/build/lib/lean/` via

```
lake env lean -R <pasta-FORMAL> <pasta-FORMAL>/<Arquivo>.lean \
  -o .lake/build/lib/lean/<Arquivo>.olean
```

(rodado a partir de `05_FORMAL/lean`, escrevendo SOMENTE no diretório
`.lake/` ignorado pelo git; `PVFunctionalOnArbitraryCompactK.olean` já
estava presente no cache compartilhado quando esta sessão começou,
`PVEnvelopeCrossCompactMonotonicity.olean` foi compilado por esta sessão
antes de escrever este arquivo). Isso permite `import
PVEnvelopeCrossCompactMonotonicity` abaixo (que por sua vez importa
`PVFunctionalOnArbitraryCompactK`), evitando restatar as ~1300+ linhas
de maquinária de NS-1/NS-2a/NS-2b/NS-3a/NS-4a/NS-5a que este arquivo não
modifica. O CONTEÚDO de NS-4a e NS-5a permanece intocado (nenhum arquivo
fora deste é editado por esta sessão); só os artefatos de build,
gitignored, foram preenchidos no cache compartilhado, exatamente como
documentado como aceitável no protocolo desta onda. O único conteúdo
NOVO desta frente são `autoEnvelopeRadius`, `autoEnvelopeRadius_pos`,
`autoEnvelopeRadius_subset` (as três peças auxiliares de derivação do
raio a partir da compacidade) e o teorema-alvo
`pvKCLM_cross_compact_monotone_auto_radius` — nenhuma outra
definição/teorema é declarado neste arquivo.
-/

import PVEnvelopeCrossCompactMonotonicity

namespace TamesisNSPVCrossCompactMonotonicityAutoRadius

open TamesisNSPVFunctionalOnArbitraryK
open TamesisNSPVEnvelopeCrossCompactMonotonicity
open TopologicalSpace MeasureTheory

/-! ## NOVO NESTA FRENTE (NS-6a)

Único conteúdo novo desta sessão: as três peças auxiliares de derivação
do raio-envelope a partir da compacidade do próprio compacto
(`autoEnvelopeRadius`, `autoEnvelopeRadius_pos`,
`autoEnvelopeRadius_subset`) e o teste falsificável do plano de ataque,
`pvKCLM_cross_compact_monotone_auto_radius`, provado por instanciação
direta de `pvKCLM_cross_compact_monotone` (NS-5a) com esses raios
auto-derivados. -/

/-- Raio-envelope AUTO-DERIVADO de um compacto `K : Compacts E`: existe
(Mathlib, `IsCompact.isBounded` + `Bornology.IsBounded.subset_closedBall_lt`,
com limiar `0` e centro `0`) porque `K` é compacto, logo limitado — este
raio nunca é escolhido livremente por um chamador, é extraído de `K`
via `Classical.choose`. -/
noncomputable def autoEnvelopeRadius
    (K : Compacts (EuclideanSpace ℝ (Fin 3))) : ℝ :=
  (K.isCompact.isBounded.subset_closedBall_lt 0 0).choose

/-- O raio auto-derivado é estritamente positivo (metade esquerda da
conjunção extraída de `Bornology.IsBounded.subset_closedBall_lt`). -/
theorem autoEnvelopeRadius_pos
    (K : Compacts (EuclideanSpace ℝ (Fin 3))) :
    0 < autoEnvelopeRadius K :=
  (K.isCompact.isBounded.subset_closedBall_lt 0 0).choose_spec.1

/-- `K` está contido, na ordem de `Compacts E`, na bola-envelope de raio
auto-derivado (metade direita da conjunção, convertida de inclusão bruta
de conjuntos para a ordem de `Compacts E` via `SetLike.coe_subset_coe`;
`(pvKCompact R : Set E)` é definicionalmente `Metric.closedBall 0 R`,
NS-4a). -/
theorem autoEnvelopeRadius_subset
    (K : Compacts (EuclideanSpace ℝ (Fin 3))) :
    K ≤ pvKCompact (autoEnvelopeRadius K) :=
  SetLike.coe_subset_coe.mp
    (K.isCompact.isBounded.subset_closedBall_lt 0 0).choose_spec.2

/-- **Teorema-alvo (NS-6a).** Monotonicidade cruzada-compacta com raio
auto-derivado: para dois compactos DECLARADOS DIFERENTES `K1 ≤ K2` e
uma função-teste `f ∈ 𝓓^{1}_{K1}(E, ℝ)`, o valor de `pvKCLM` aplicado à
inclusão DIRETA `K1 → envelope(K1)` é igual ao valor de `pvKCLM`
aplicado à inclusão em DOIS PASSOS `K1 → K2 → envelope(K2)`, onde
`envelope(K)` é a bola-envelope de raio `autoEnvelopeRadius K`, DERIVADO
inteiramente da compacidade de `K` — nenhuma hipótese de raio ou de
inclusão-em-bola aparece como argumento livre deste enunciado (compare
com `pvKCLM_cross_compact_monotone`, NS-5a, cujo enunciado toma `R1 R2 :
ℝ`, `hR1 : 0 < R1`, `hR2 : 0 < R2`, `hK1R1`, `hK2R2` como hipóteses
livres). Consequência de instanciar `pvKCLM_cross_compact_monotone`
(NS-5a) com `R1 := autoEnvelopeRadius K1`, `R2 := autoEnvelopeRadius
K2`. -/
theorem pvKCLM_cross_compact_monotone_auto_radius
    (e2 e3 : EuclideanSpace ℝ (Fin 3))
    (K1 K2 : Compacts (EuclideanSpace ℝ (Fin 3)))
    (hK1K2 : K1 ≤ K2)
    (f : ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K1) :
    pvKCLM e2 e3 (autoEnvelopeRadius K1) (autoEnvelopeRadius_pos K1)
        (ContDiffMapSupportedIn.monoCLM ℝ f :
          ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞)
            (pvKCompact (autoEnvelopeRadius K1)))
      = pvKCLM e2 e3 (autoEnvelopeRadius K2) (autoEnvelopeRadius_pos K2)
        (ContDiffMapSupportedIn.monoCLM ℝ
            (ContDiffMapSupportedIn.monoCLM ℝ f :
              ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞) K2) :
          ContDiffMapSupportedIn (EuclideanSpace ℝ (Fin 3)) ℝ (1 : ℕ∞)
            (pvKCompact (autoEnvelopeRadius K2))) :=
  pvKCLM_cross_compact_monotone e2 e3 K1 K2
    (autoEnvelopeRadius K1) (autoEnvelopeRadius K2)
    (autoEnvelopeRadius_pos K1) (autoEnvelopeRadius_pos K2)
    hK1K2 (autoEnvelopeRadius_subset K1) (autoEnvelopeRadius_subset K2) f

#print axioms autoEnvelopeRadius_pos
#print axioms autoEnvelopeRadius_subset
#print axioms pvKCLM_cross_compact_monotone_auto_radius

end TamesisNSPVCrossCompactMonotonicityAutoRadius

/-! ## O que NÃO é afirmado

```text
NÃO constrói um membro de `𝓓^{1}(E, ℝ) →L[ℝ] ℝ` (dual topológico do
  espaço COMPLETO de funções-teste) -- mesmo gap (iii) já escopado para
  fora em NS-4a/NS-5a, inteiramente fora do escopo desta frente também
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
NÃO afirma novidade matemática -- é uma consequência elementar de (a)
  `IsCompact.isBounded` + `Bornology.IsBounded.subset_closedBall_lt`
  (Mathlib) garantindo que todo compacto tem ALGUM raio-envelope, e (b)
  instanciar `pvKCLM_cross_compact_monotone` (NS-5a, já fechado) com
  esse raio -- nenhum "diamante de composição" novo, nenhuma análise
  nova: o CONTEÚDO matemático é idêntico a NS-5a, só a APRESENTAÇÃO do
  enunciado muda (os dois raios deixam de ser hipóteses livres e passam
  a ser termos derivados internamente via `Classical.choose`)
NÃO afirma que o raio `autoEnvelopeRadius K` é o raio ÓTIMO/mínimo para
  `K` -- `Bornology.IsBounded.subset_closedBall_lt` só garante EXISTÊNCIA
  de algum raio, escolhido não-construtivamente por `Classical.choose`;
  `autoEnvelopeRadius` não é computável (`noncomputable`) e não tem
  fórmula fechada em termos de `K`
NÃO modifica `PVFunctionalOnArbitraryCompactK.lean` (NS-4a) nem
  `PVEnvelopeCrossCompactMonotonicity.lean` (NS-5a) nem qualquer outro
  arquivo de onda anterior -- só seus artefatos de build `.olean`
  (gitignored) foram preenchidos no cache compartilhado
  `05_FORMAL/lean/.lake/build/lib/lean/`, para permitir `import` direto
  em vez de restatação verbatim de mais de 1300 linhas
```
-/
