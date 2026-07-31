---
status: SIGNATURES_ELABORATED_NO_PROOFS
lean: "leanprover/lean4:v4.33.0-rc1"
mathlib_revision: "79d0395a1825a6264ad5d269e35e60537518955e"
---

# Viabilidade Lean da ponte

## SignatureProbe

`05_FORMAL/lean/TamesisLab/RHNogo/Bridge/SignatureProbe.lean`

Contém **apenas** definições, estruturas e `#check`. Nenhuma prova da ponte;
`ASYM-NOGO-001` **não** é aplicado; operadores, lei de Weyl e `ζ` não são
mencionados. `set_option autoImplicit false` está ativo, para que nenhum
identificador desconhecido seja capturado silenciosamente como variável
universal (o erro que ocorreu no gate `ASYM-NOGO-001`).

Estado: `lake env lean` exit 0; `lake build` PASS com **8.692 jobs**; tokens
proibidos zero.

## Assinaturas elaboradas

```text
PowerCountingLaw           : (ℝ → ℝ) → Type
TLogCountingLaw            : (ℝ → ℝ) → Type
SubdominantDifference      : (ℝ → ℝ) → (ℝ → ℝ) → Prop
EventualEquality           : (ℝ → ℝ) → (ℝ → ℝ) → Prop
BoundedDifference          : (ℝ → ℝ) → (ℝ → ℝ) → Prop
RatioEquivalence           : (ℝ → ℝ) → (ℝ → ℝ) → Prop
CountingLawBridgeStatement : Prop
NarrowSpectralNogoStatement: Prop
```

Nota de projeto: `PowerCountingLaw` e `TLogCountingLaw` elaboram em `Type`,
não em `Prop`, porque **carregam dados** (`exponent`, `constant`) além das
hipóteses. Isto é deliberado e corresponde à definição de `W-POWER`, que é
uma tripla `(N, α, C)` mais as três suposições — não uma mera proposição.

## Ferramentas Mathlib verificadas por `#check`

| Ferramenta | Assinatura confirmada |
|---|---|
| `Asymptotics.IsLittleO.tendsto_div_nhds_zero` | `f =o[l] g → Tendsto (fun x => f x / g x) l (nhds 0)` |
| `Filter.Tendsto.add` | soma de limites |
| `Filter.Tendsto.congr'` | transporte por igualdade eventual |

Somadas às já usadas em `ASYM-NOGO-001` (`Real.log`, `Real.rpow`,
`isLittleO_log_rpow_atTop`, `tendsto_nhds_unique`,
`Filter.Tendsto.pos_mul_atTop`, `not_tendsto_nhds_of_tendsto_atTop`), o
ferramental está completo para o próximo gate.

## Estratégia prevista para `CountingLawBridgeStatement` (não executada)

1. Reescrever eventualmente
   `NP T/(T log T) = (NP T − Nzeta T)/(T log T) + Nzeta T/(T log T)`
   — identidade algébrica válida onde `T log T ≠ 0`, isto é, para `T > 1`
   (`eventually_gt_atTop`).
2. `IsLittleO.tendsto_div_nhds_zero` aplicado à hipótese E2 dá
   `(NP − Nzeta)/(T log T) → 0`.
3. `Filter.Tendsto.add` com a hipótese sobre `Nzeta` dá limite `0 + c = c`.
4. `Filter.Tendsto.congr'` transporta pela identidade eventual da etapa 1.

Complexidade estimada: **baixa** — mesma forma da
`eventually_normalization_identity` já verificada. Sem `ζ`, sem operadores,
sem EDP, sem `π`.

## Estratégia prevista para `NarrowSpectralNogoStatement` (não executada)

Composição direta: `TLogCountingLaw Nzeta` + `SubdominantDifference` +
`CountingLawBridge` dá `TLogCountingLaw NP`; junto com `PowerCountingLaw NP`,
`asym_nogo_001` fecha em `False`.

**Não executada.** A aplicação de `ASYM-NOGO-001` está explicitamente fora
da autorização deste gate.

## Riscos

1. Contabilidade de filtros na identidade algébrica eventual (`T log T ≠ 0`
   exige `T > 1`) — já resolvida no gate anterior, mesmo padrão.
2. `IsLittleO` sobre `NormedDivisionRing`: `ℝ` satisfaz; confirmado pela
   assinatura no `#check`.
3. Nenhum risco de dependência externa: nada além de `Filter`, `Real.log`,
   `Real.rpow` e `Asymptotics`.

## Limite explícito

O que é formalizável **agora** é apenas o segmento abstrato:

```text
W-POWER  +  TLOG  +  E2   ⟹   contradicao
```

Os dois ramos que ligam esse segmento à matemática real —
`GLOBAL-WEYL-BRIDGE-SCALAR` (operadores) e `RVM-LIMIT` (`ζ`) — **não são
formalizáveis** com as autorizações vigentes, e o segundo provavelmente
permanecerá fora de alcance por muito tempo (`SB-GAP-010`).
