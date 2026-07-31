# RH-NOGO-001 — Viabilidade Lean do núcleo abstrato

Inspeção do checkout fixado da Mathlib
(revisão `79d0395a1825a6264ad5d269e35e60537518955e`), realizada em
2026-07-31. Somente o núcleo `ASYM-NOGO-001` é avaliado; PDE, lei de Weyl
e zeta ficam fora da formalização autorizada.

## Ferramentas verificadas no checkout

| Ferramenta | Módulo | Verificação |
|---|---|---|
| `Filter.Tendsto`, `Filter.atTop`, `nhds` | núcleo de `Mathlib.Order.Filter` / topologia | presente (uso pervasivo) |
| `Real.log`, `Real.tendsto_log_atTop` | `Mathlib/Analysis/SpecialFunctions/Log/Basic.lean` (linha ~351) | grep confirmado |
| `Real.rpow` (`T ^ α`) | `Mathlib/Analysis/SpecialFunctions/Pow/Real.lean` | presente |
| `Asymptotics.IsBigO`, `IsLittleO`, `IsBigOWith` | `Mathlib/Analysis/Asymptotics/Defs.lean` (linhas ~91–103) | grep confirmado |
| `isLittleO_log_rpow_atTop : 0 < r → Real.log =o[atTop] fun x => x ^ r` | `Mathlib/Analysis/SpecialFunctions/Pow/Asymptotics.lean` (linha ~364) | assinatura confirmada por `#check` no probe — **namespace raiz**, nao `Real.` (correcao de uma primeira tentativa que falhou com `unknownIdentifier`) |
| `tendsto_rpow_atTop` | `Mathlib/Analysis/SpecialFunctions/Pow/Asymptotics.lean` | grep confirmado (usado na prova do item anterior) |
| `Filter.Tendsto.div`, `tendsto_nhds_unique` | análise/topologia básicas | presentes (padrão) |

## Assinatura candidata (registrada sem prova)

`TamesisLab/RHNogo/SignatureProbe.lean` define

```lean
def AsymNogoStatement : Prop :=
  ∀ (N : ℝ → ℝ) (c C α : ℝ), 0 < c → 0 < C → 0 < α →
    Filter.Tendsto (fun T => N T / (T * Real.log T)) Filter.atTop (nhds c) →
    ¬ Filter.Tendsto (fun T => N T / T ^ α) Filter.atTop (nhds C)
```

como `Prop` **sem corpo probatório**, apenas para verificar que a
assinatura elabora contra a Mathlib fixada. O arquivo está no grafo de
build e compila (`lake env lean` exit 0; `lake build` 8.684 jobs). Os
`#check` do probe imprimem as assinaturas exatas das ferramentas previstas,
o que já corrigiu um erro de namespace antes de qualquer prova.

## Estratégia (resumo; detalhe em `ASYMPTOTIC_CORE.md`)

Quociente das duas hipóteses → limite finito positivo `C/c` para
`log T · T^{1−α}` — contradito por `isLittleO_log_rpow_atTop` (α > 1) ou
por divergência (`α ≤ 1`).

## Riscos identificados

1. Manipulação de `rpow` com expoentes reais exige lemas de positividade
   eventual (`T > 0`, `log T > 0`, `N T ≠ 0` eventualmente) — disponíveis
   (`eventually_gt_atTop`), mas com contabilidade de filtros.
2. A álgebra dos quocientes (`N/T^α = (N/(T log T)) · (log T · T^{1−α})`
   eventualmente) exige `Filter.EventuallyEq` cuidadoso.
3. Nenhum risco de dependência externa: o núcleo não usa zeta, PDE nem π.

Avaliação: **viável** com as ferramentas existentes; complexidade estimada
baixa-média (um arquivo, um teorema, lemas auxiliares locais).
