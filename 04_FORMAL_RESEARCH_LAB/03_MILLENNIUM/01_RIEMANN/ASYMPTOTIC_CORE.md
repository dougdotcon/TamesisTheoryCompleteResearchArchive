# RH-NOGO-001 — Núcleo assintótico abstrato (ASYM-NOGO-001)

Sublema independente de PDE, candidato a núcleo Lean futuro.
**Não formalizado neste gate** — apenas enunciado, casos, assinatura
candidata e estratégia.

## Enunciado

> **ASYM-NOGO-001.** Não existe função `N : ℝ → ℝ` que satisfaça
> simultaneamente:
>
> A. `N(T) / (T · log T) → c` quando `T → ∞`, com `c > 0`;
>
> B. `N(T) / T^α → C` quando `T → ∞`, com `C > 0` e `α > 0` fixo.

Observações:

- A constante `c` é abstrata; na aplicação, `c = 1/(2π)`. O valor exato é
  irrelevante — só a positividade é usada. Isso remove `π` das dependências
  Lean do núcleo.
- `N` não precisa ser monótona, inteira ou de contagem: o lema vale para
  qualquer função real. A interpretação como contagem entra apenas na
  aplicação futura.
- A conclusão usada na aplicação é a contrapositiva: se A vale
  (Riemann–von Mangoldt) então B falha para todos `α, C > 0` (Weyl).

## Análise de casos

Escreva `Q(T) := N(T) / (T log T) → c > 0`.

| Caso | Argumento |
|---|---|
| `α = 1` | `N(T)/T = Q(T) · log T → c · ∞ = ∞ ≠ C` (divergência do fator `log`) |
| `α > 1` | `N(T)/T^α = Q(T) · log T · T^{1−α} → c · 0 = 0 ≠ C` (pois `log T · T^{1−α} → 0`; `log =o` de qualquer potência positiva) |
| `α < 1` | `N(T)/T^α = Q(T) · log T · T^{1−α} → ∞ ≠ C` (potência positiva vezes `log`) |

Os três casos reduzem-se a um único fato:
`log T · T^{1−α}` tende a `∞` (α ≤ 1) ou a `0` (α > 1), nunca a um limite
finito positivo — logo `N/T^α` não pode ter limite finito positivo se
`N/(T log T)` tem.

## Assinatura Lean candidata

```lean
theorem asym_nogo (N : ℝ → ℝ) (c C α : ℝ)
    (hc : 0 < c) (hC : 0 < C) (hα : 0 < α)
    (hA : Filter.Tendsto (fun T => N T / (T * Real.log T))
            Filter.atTop (nhds c))
    (hB : Filter.Tendsto (fun T => N T / T ^ α)
            Filter.atTop (nhds C)) : False
```

(`T ^ α` é `Real.rpow`.) O enunciado está registrado como `Prop` sem prova
em `TamesisLab/RHNogo/SignatureProbe.lean`, que compila contra a Mathlib
fixada.

## Estratégia de prova prevista (futura, não executada)

1. De `hA` e `hB`, formar o quociente
   `(N/T^α) / (N/(T log T)) = log T · T^{1−α}` eventualmente (onde
   `N T ≠ 0`, garantido eventualmente por `hA` com `c > 0`).
2. `Filter.Tendsto.div hB hA (ne_of_gt hc)` dá limite finito `C/c > 0`
   para o quociente.
3. Contradizer com o comportamento de `log T · T^{1−α}`:
   - `α > 1`: `Real.isLittleO_log_rpow_atTop` (com `r := α − 1`) dá
     `log =o[atTop] T^{α−1}`, logo o produto tende a 0 — contradição com
     limite `C/c > 0` via unicidade de limites (`tendsto_nhds_unique`).
   - `α ≤ 1`: `Real.tendsto_log_atTop` e `tendsto_rpow_atTop`
     (ou `T^{1−α} ≥ 1` eventualmente) dão divergência — contradição com
     limite finito.
4. Alternativa mais uniforme: comparar `hA` e `hB` diretamente via
   `Asymptotics.IsLittleO`/`IsBigO` entre `T^α` e `T log T`.

Dependências Mathlib verificadas no checkout fixado: ver
`LEAN_FEASIBILITY.md`.

## Papel na arquitetura

```text
ASYM-NOGO-001 (abstrato, formalizável primeiro)
        ↑ tradução (GAP-RH-003)
Riemann–von Mangoldt (A com c = 1/2π)   +   Weyl na Classe W (B com α = d/m)
        ⟹ exclusão da Classe W (RH-NOGO-001)
```

A formalização autorizada pelo próximo gate cobre **somente** a caixa
superior.
