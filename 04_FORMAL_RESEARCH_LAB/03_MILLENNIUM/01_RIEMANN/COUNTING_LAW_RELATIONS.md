---
status: SPECIFIED_NOT_PROVED
central_level: E2
---

# Relações entre as duas funções de contagem — níveis E0–E3

O alvo **não** é a igualdade exata. Quatro níveis, do mais forte ao mais
fraco relevante.

## E0 — igualdade eventual

```text
∀ᶠ T in atTop, N_P(T) = N_ζ(T)
```

Assinatura candidata:

```lean
def EventualEquality (N M : ℝ → ℝ) : Prop :=
  ∀ᶠ T in atTop, N T = M T
```

## E1 — discrepância limitada

```text
N_P(T) − N_ζ(T) = O(1)
```

```lean
def BoundedDifference (N M : ℝ → ℝ) : Prop :=
  Asymptotics.IsBigO atTop (fun T => N T - M T) (fun _ => (1 : ℝ))
```

## E2 — discrepância subdominante  ← **nível central**

```text
N_P(T) − N_ζ(T) = o(T log T)
```

```lean
def SubdominantDifference (N M : ℝ → ℝ) : Prop :=
  Asymptotics.IsLittleO atTop
    (fun T => N T - M T) (fun T => T * Real.log T)
```

## E3 — equivalência por razão

```text
N_P(T) / N_ζ(T) → 1
```

```lean
def RatioEquivalence (N M : ℝ → ℝ) : Prop :=
  Tendsto (fun T => N T / M T) atTop (nhds 1)
```

Hipóteses necessárias para o denominador: `M T ≠ 0` eventualmente. Sob
`RVM-LIMIT` (`N_ζ/(T log T) → 1/2π > 0`) isso vale eventualmente, mas é uma
**obrigação separada**, não automática.

---

## Hierarquia pretendida

```text
E0 ⇒ E1 ⇒ E2
E3 ⇒ E2
```

| Seta | Justificativa esboçada (NÃO provada) | Hipóteses extras |
|---|---|---|
| `E0 ⇒ E1` | diferença eventualmente nula é eventualmente limitada | — |
| `E1 ⇒ E2` | `O(1) = o(T log T)` porque `T log T → +∞` | `T log T → ∞` (vale) |
| `E3 ⇒ E2` | `N_P − N_ζ = N_ζ·(N_P/N_ζ − 1) = o(1)·N_ζ` e `N_ζ = O(T log T)` | `N_ζ ≠ 0` eventualmente; `N_ζ/(T log T)` limitada |

**Nenhuma seta é provada neste gate.**

## Por que E2 é o nível central

1. **Cobre os outros três.** Provar o no-go sob E2 exclui automaticamente
   E0, E1 e E3.
2. **É robusto.** Não depende de convenções de fronteira (`<` versus `≤`),
   de multiplicidade em pontos isolados, nem de deslocamentos limitados:
   qualquer discrepância `O(1)` é absorvida.
3. **É o mínimo que a contradição precisa.** O `COUNTING-LAW-BRIDGE`
   transporta a lei `T log T` de `N_ζ` para `N_P` exatamente sob E2 — nem
   mais nem menos.
4. **É matematicamente mais forte como resultado negativo.** Exclui não só
   coincidência espectral perfeita, mas qualquer modelo da classe cuja
   contagem difira da dos zeros por termo subdominante.

## O que E2 NÃO significa

E2 **não** afirma que os espectros coincidem. Duas funções de contagem podem
satisfazer E2 com multiconjuntos muito diferentes. A implicação vai só num
sentido: igualdade espectral ⟹ E0 ⟹ E2 (ver
`SPECTRAL_MATCH_CONVENTIONS.md`), **nunca** o contrário.
