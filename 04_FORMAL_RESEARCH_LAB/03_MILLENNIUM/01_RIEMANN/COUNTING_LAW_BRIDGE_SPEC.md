---
lemma_id: COUNTING-LAW-BRIDGE
status: SPECIFIED_NOT_PROVED
---

# COUNTING-LAW-BRIDGE — especificação

## Enunciado

```text
Se

  N_ζ(T) / (T log T) → c,   com c > 0,

e

  N_P(T) − N_ζ(T) = o(T log T),

então

  N_P(T) / (T log T) → c.
```

## Por que uma só ponte, e não quatro

Esta formulação cobre de uma vez:

| Nível | Como é absorvido |
|---|---|
| E0 igualdade eventual | diferença eventualmente nula ⟹ `o(T log T)` |
| E1 discrepância `O(1)` | `O(1) ⟹ o(T log T)` |
| E2 discrepância subdominante | hipótese literal |
| E3 equivalência por razão | `E3 ⟹ E2` (com `N_ζ ≠ 0` eventualmente) |

Criar um lema por nível multiplicaria a superfície de prova sem ganho. A
ponte única é preferível.

## Esboço da justificativa — NÃO é prova

```text
N_P(T)/(T log T)
  = N_ζ(T)/(T log T)  +  (N_P(T) − N_ζ(T))/(T log T)
  →  c  +  0
  =  c
```

A segunda parcela tende a zero **por definição** de `o(T log T)`. Registrado
como esboço; a prova formal pertence ao próximo gate.

## Assinatura Lean candidata (não implementada)

```lean
def CountingLawBridgeStatement : Prop :=
  ∀ (NP Nzeta : ℝ → ℝ) (c : ℝ), 0 < c →
    Tendsto (fun T => Nzeta T / (T * Real.log T)) atTop (nhds c) →
    Asymptotics.IsLittleO atTop
      (fun T => NP T - Nzeta T) (fun T => T * Real.log T) →
    Tendsto (fun T => NP T / (T * Real.log T)) atTop (nhds c)
```

Registrada em `TamesisLab/RHNogo/Bridge/SignatureProbe.lean` como `Prop`
**sem corpo probatório**.

## Ferramentas Mathlib previstas

| Ferramenta | Papel |
|---|---|
| `Asymptotics.IsLittleO` | hipótese E2 |
| `Asymptotics.IsLittleO.tendsto_div_nhds_zero` | segunda parcela → 0 |
| `Filter.Tendsto.add` | soma dos limites |
| `Filter.Tendsto.congr'` | identidade algébrica eventual `(a−b+b)/x = (a−b)/x + b/x` |
| `Real.log`, `Filter.atTop`, `nhds` | núcleo |

Todas presentes na revisão fixada `79d0395a…` — verificadas no gate
`ASYM-NOGO-001`, que usou o mesmo conjunto.

## Dificuldade estimada

**Baixa.** A prova é uma soma de limites com uma reescrita algébrica
eventual. Comparável em porte ao `eventually_normalization_identity` já
verificado. Nenhuma teoria nova é necessária: sem `ζ`, sem operadores, sem
EDP, sem `π`.

## Papel na cadeia

```text
RVM-LIMIT  (c = 1/2π para N_ζ)
     +
E2         (N_P − N_ζ = o(T log T))
     ↓  COUNTING-LAW-BRIDGE
TLOG-LAW-FOR-NP  (N_P/(T log T) → 1/2π)
     +
POWER-LAW-FOR-NP (N_P/T^{d/m} → C_P > 0, via GLOBAL-WEYL-BRIDGE)
     ↓  ASYM-NOGO-001
False
```

**Nada disso foi executado.**
